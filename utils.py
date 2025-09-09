import time, json, random, sqlite3
from pathlib import Path
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import streamlit as st

# -----------------------
# Configuration / storage
# -----------------------
DATA_DIR = Path("./data")
IMAGES_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "db.sqlite"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# create or connect sqlite DB
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# tables
c.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    tag TEXT,
    uploaded_at REAL,
    colors TEXT,
    notes TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS ootd_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ootd_filename TEXT,
    suggested_item_id INTEGER,
    feedback INTEGER,
    timestamp REAL
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS bandit_stats (
    item_id INTEGER PRIMARY KEY,
    plays INTEGER DEFAULT 0,
    rewards INTEGER DEFAULT 0
)
""")
conn.commit()

# -----------------------
# Utilities
# -----------------------
def save_image(uploaded_file, prefix="item"):
    ext = Path(uploaded_file.name).suffix or ".jpg"
    ts = int(time.time()*1000)
    filename = f"{prefix}_{ts}{ext}"
    path = IMAGES_DIR / filename
    image = Image.open(uploaded_file).convert("RGB")
    image.save(path)
    return str(path.name)

def extract_dominant_colors(image_pil, k=4, resize=(150,150)):
    arr = np.array(image_pil.resize(resize))
    pixels = arr.reshape(-1, 3).astype(float)
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(int).tolist()
    return centers

def display_color_patches(colors, width=40, height=40):
    cols = st.columns(len(colors))
    for col, c in zip(cols, colors):
        r,g,b = c
        hexc = '#%02x%02x%02x' % (r,g,b)
        col.markdown(f'<div style="width:{width}px;height:{height}px;background:{hexc};border-radius:6px;"></div>', unsafe_allow_html=True)

def item_row(item):
    st.write(f"**#{item[0]}** — Tag: *{item[2]}* — uploaded: {time.ctime(item[3])}")
    img_path = IMAGES_DIR / item[1]
    st.image(str(img_path), width=220)
    colors = json.loads(item[4]) if item[4] else []
    if colors:
        display_color_patches(colors)

def get_all_items(tag_filter=None):
    if tag_filter:
        cur = c.execute("SELECT * FROM items WHERE tag = ? ORDER BY uploaded_at DESC", (tag_filter,))
    else:
        cur = c.execute("SELECT * FROM items ORDER BY uploaded_at DESC")
    return cur.fetchall()

def add_item_record(filename, tag, colors, notes=""):
    now = time.time()
    c.execute("INSERT INTO items (filename, tag, uploaded_at, colors, notes) VALUES (?, ?, ?, ?, ?)",
              (filename, tag, now, json.dumps(colors), notes))
    item_id = c.lastrowid
    c.execute("INSERT OR IGNORE INTO bandit_stats (item_id, plays, rewards) VALUES (?, 0, 0)", (item_id,))
    conn.commit()
    return item_id

def suggest_items_epsilon_greedy(k=3, eps=0.2, tag=None):
    rows = get_all_items(tag_filter=tag)
    if not rows:
        return []
    stats = {}
    for r in rows:
        item_id = r[0]
        srow = c.execute("SELECT plays, rewards FROM bandit_stats WHERE item_id=?", (item_id,)).fetchone()
        if srow:
            plays, rewards = srow
        else:
            plays, rewards = 0,0
            c.execute("INSERT OR IGNORE INTO bandit_stats (item_id, plays, rewards) VALUES (?, ?, ?)", (item_id,0,0))
            conn.commit()
        stats[item_id] = (plays, rewards)

    chosen = []
    for _ in range(min(k, len(rows))):
        if random.random() < eps:
            candidate = random.choice([r for r in rows if r[0] not in chosen])
            chosen.append(candidate[0])
        else:
            best_item = None
            best_score = -1
            for r in rows:
                iid = r[0]
                plays, rewards = stats.get(iid,(0,0))
                score = (rewards / plays) if plays>0 else 0.0
                if iid in chosen:
                    continue
                if score > best_score:
                    best_score = score
                    best_item = iid
            if best_item is None:
                candidate = random.choice([r for r in rows if r[0] not in chosen])
                chosen.append(candidate[0])
            else:
                chosen.append(best_item)
    chosen_rows = [r for r in rows if r[0] in chosen]
    ordered = []
    for iid in chosen:
        for r in chosen_rows:
            if r[0]==iid:
                ordered.append(r)
                break
    return ordered

def update_bandit_stats(item_id, reward):
    c.execute("INSERT OR IGNORE INTO bandit_stats (item_id, plays, rewards) VALUES (?, 0, 0)", (item_id,))
    c.execute("UPDATE bandit_stats SET plays = plays + 1, rewards = rewards + ? WHERE item_id = ?", (reward, item_id))
    conn.commit()
