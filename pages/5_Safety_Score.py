import streamlit as st
import requests
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR

st.title("🛡️ Women's Safety Score by Location")

location = st.text_input("📍 Enter your location (City, Country)")

if st.button("Check Safety Score"):
    st.write(f"🔍 Fetching crime/safety data for {location}...")
    st.info("📌 Placeholder: Connect to real public safety datasets or APIs.")
    st.warning("⚠️ Demo only: Showing dummy safety score.")

    st.metric(label="Safety Score (0-100)", value="62", delta="-5 vs last year")
