import streamlit as st
from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.title("SmartWardrobe: Upload Your Wardrobe Picture")


uploaded_file = st.file_uploader("Upload a JPG image of your wardrobe", type=["jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Wardrobe", use_column_width=True)

    # img to array
    img_array = np.array(image)
    # img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Resize
    resized_img = cv2.resize(img_array, (200, 200))
    reshaped_img = resized_img.reshape((-1, 3))

    # KMeans to find dominant colors
    k = 5
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(reshaped_img)
    colors = kmeans.cluster_centers_.astype(int)

    st.subheader("Dominant Colors in Your Wardrobe")
    fig, ax = plt.subplots(1, k, figsize=(12, 3))
    for i in range(k):
        color_patch = np.zeros((100, 100, 3), dtype=np.uint8)
        color_patch[:, :] = colors[i]
        ax[i].imshow(color_patch)
        ax[i].axis("off")
    st.pyplot(fig)

    #insights 
    avg_brightness = np.mean(cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)[:, :, 2])
    if avg_brightness > 120:
        st.write("Your wardrobe tends to have **bright/vibrant clothing**.")
    else:
        st.write("Your wardrobe tends to have **muted/darker clothing**.")

