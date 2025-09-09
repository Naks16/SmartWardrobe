import streamlit as st
import requests
import os
from urllib.parse import quote_plus
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Style Inspiration", page_icon="🎨", layout="wide")
st.title("🎨 Style Inspiration (Pinterest API)")

# Cached fetch to avoid repeated calls
@st.cache_data(ttl=3600)
def fetch_style_pins(query, limit=9):
    api_key = os.getenv("SCRAPE_CREATORS_API_KEY")
    
    if not api_key:
        raise RuntimeError("⚠️ Missing API key! Add SCRAPE_CREATORS_API_KEY to st.secrets or env vars.")

    url_q = quote_plus(query)
    url = f"https://api.scrapecreators.com/v1/pinterest/search?query={url_q}&limit={limit}"
    headers = {"x-api-key": api_key}

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    pins = data.get("pins") or data.get("data") or data.get("results") or []
    images = []
    for p in pins:
        if not isinstance(p, dict):
            continue
        img_url = None
        imgs = p.get("images") or {}
        if isinstance(imgs, dict):
            orig = imgs.get("orig") or imgs.get("original") or next(iter(imgs.values()), None)
            if isinstance(orig, dict):
                img_url = orig.get("url") or orig.get("src")
        img_url = img_url or p.get("image") or p.get("image_url") or p.get("url") or p.get("link")
        title = p.get("title") or p.get("description") or p.get("note") or ""
        if img_url:
            images.append({"image_url": img_url, "title": title})
    return images[:limit]


# --- User Inputs ---
mood = st.text_input("🌸 Enter your mood (e.g., happy, chill, bold)")
company = st.text_input("👭 Who are you with? (e.g., friends, date, work)")
aesthetic = st.text_input("✨ Aesthetic preference (e.g., minimal, boho, chic)")

if st.button("Get Style Ideas"):
    query = f"{mood} {company} {aesthetic} women's fashion".strip()
    if not query.strip():
        st.warning("⚠️ Please enter some details first.")
    else:
        st.write(f"🔍 Searching Pinterest for: **{query}**")
        with st.spinner("Fetching ideas..."):
            try:
                pins = fetch_style_pins(query, limit=9)
            except Exception as e:
                st.error(f"❌ Failed to fetch: {e}")
                pins = []

        if not pins:
            st.info("No results found. Try different words (e.g., 'casual outfit').")
        else:
            st.success(f"✅ Found {len(pins)} style ideas!")
            cols = st.columns(3)
            for idx, pin in enumerate(pins):
                with cols[idx % 3]:
                    st.image(pin["image_url"], caption=pin["title"][:80], use_column_width=True)

