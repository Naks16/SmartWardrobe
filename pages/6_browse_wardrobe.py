import streamlit as st
from utils import get_all_items, item_row  # make sure utils.py has these
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR

st.header("Your Wardrobe")

tag_filter = st.selectbox("Filter by tag", ["All","tshirt","shirt","dress","skirt","shoes","jacket","accessory","other"])
items = get_all_items(tag_filter=None if tag_filter=="All" else tag_filter)

if not items:
    st.info("No items yet. Add some from Upload Item.")
else:
    for it in items:
        item_row(it)
        st.write("---")
