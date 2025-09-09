import streamlit as st
import json
import os
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR

st.title("📸 Upload Outfit of the Day (OOTD)")

DB_FILE = "ootd_feedback.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

uploaded_ootd = st.file_uploader("Upload your OOTD", type=["jpg", "png", "jpeg"])

if uploaded_ootd:
    st.image(uploaded_ootd, caption="Your OOTD", use_column_width=True)

    rating = st.slider("⭐ Rate this OOTD (1=Bad, 5=Great)", 1, 5, 3)
    feedback = st.text_area("💬 Why did you rate it this way?")

    if st.button("Save Feedback"):
        new_entry = {"ootd_file": uploaded_ootd.name, "rating": rating, "feedback": feedback}
        with open(DB_FILE, "r") as f:
            db = json.load(f)
        db.append(new_entry)
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
        st.success("✅ Feedback saved!")

st.markdown("### 🔁 Reinforcement Learning Placeholder")
st.info("Later: Use RL to learn what outfits you like and improve recommendations.")
