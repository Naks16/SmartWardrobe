import streamlit as st
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR

st.set_page_config(
    page_title="SmartWardrobe",
    page_icon="👗",
    layout="wide",                  # use wide layout
    initial_sidebar_state="expanded"  # force sidebar open
)

st.title("👗 SmartWardrobe")
st.subheader("Your personal AI-powered wardrobe assistant")

st.markdown("""
### 📌 Features
- 🔐 Sign up & OTP verification  
- 👕 Add clothes with **AI auto-tagging** (Fashion MNIST)  
- 📸 Upload **OOTD** and get feedback (Reinforcement Learning)  
- 🎨 Get **style inspiration** from Pinterest  
- 🛡️ Check **location safety score** for women  

👉 Use the sidebar to navigate between features.
""")
