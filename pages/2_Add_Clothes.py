import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import json
import os
from utils import save_image, extract_dominant_colors, display_color_patches, get_all_items, add_item_record, suggest_items_epsilon_greedy, update_bandit_stats, item_row, IMAGES_DIR

st.title("👕 Add Clothes to Wardrobe")

# Load model
model = tf.keras.models.load_model("fashion_mnist_model.h5")
class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

DB_FILE = "wardrobe_db.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

uploaded_file = st.file_uploader("Upload a clothing photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("L")
    img_resized = img.resize((28, 28))
    img_array = np.array(img_resized) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    prediction = model.predict(img_array)
    label = class_names[np.argmax(prediction)]
    st.success(f"Predicted Category: {label}")

    corrected_label = st.selectbox("Correct if wrong:", class_names, index=class_names.index(label))

    if st.button("Save to Wardrobe"):
        new_item = {"file_name": uploaded_file.name, "category": corrected_label}
        with open(DB_FILE, "r") as f:
            db = json.load(f)
        db.append(new_item)
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
        st.success(f"✅ Saved {corrected_label} to your wardrobe!")
