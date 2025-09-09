# 5_safety_score.py
import streamlit as st
import requests
import random

st.set_page_config(page_title="Women's Safety Score", page_icon="🛡️")

st.title("🛡️ Women's Safety Score by Location")
st.subheader("Get a safety assessment for your locality")

# -----------------------------
# User input
# -----------------------------
location = st.text_input("📍 Enter your location (Full address, locality, city)")

if st.button("Check Safety Score") and location:
    st.write(f"🔍 Geocoding and analyzing safety for: {location}")
    
    try:
        # -----------------------------
        # 1️⃣ Geocode using OpenStreetMap Nominatim
        # -----------------------------
        nom_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location, "format":"json", "limit":1}
        resp = requests.get(nom_url, params=params, headers={"User-Agent":"SmartWardrobe/1.0"}, timeout=10)
        if resp.ok and resp.json():
            res = resp.json()[0]
            lat, lon = float(res["lat"]), float(res["lon"])
            st.success(f"📌 Location found: {res['display_name']} ({lat:.4f}, {lon:.4f})")
        else:
            st.error("❌ Could not geocode the location. Try a more specific address.")
            st.stop()
        
        # -----------------------------
        # 2️⃣ Fetch/Simulate crime incidents & review sentiment
        # -----------------------------
        # For demo: we generate some fake numbers for crime and reviews
        num_crimes = random.randint(0, 20)           # number of reported incidents nearby
        negative_reviews = random.randint(0, 10)     # negative sentiment mentions
        positive_reviews = random.randint(0, 10)     # positive sentiment mentions
        lighting_factor = random.choice([0,5,10])    # lighting / crowd factor
        
        st.write(f"📊 Crime incidents nearby: {num_crimes}")
        st.write(f"💬 Negative reviews: {negative_reviews}, Positive reviews: {positive_reviews}")
        st.write(f"💡 Environmental factor (lighting/crowd): {lighting_factor}/10")

        # -----------------------------
        # 3️⃣ Compute Safety Score (0-100)
        # -----------------------------
        score = 100
        score -= min(num_crimes * 3, 50)            # crime weight
        score -= min(negative_reviews * 5, 25)      # negative reviews weight
        score += min(positive_reviews * 3, 15)      # positive reviews help
        score += lighting_factor                     # small bonus
        score = max(0, min(100, score))
        
        st.metric("Safety Score (0=Risky, 100=Safe)", score)
        
        # -----------------------------
        # 4️⃣ Optional feedback / advice
        # -----------------------------
        if score < 40:
            st.warning("⚠️ This area seems risky. Stay alert and avoid isolated spots.")
        elif score < 70:
            st.info("ℹ️ Moderate safety. Exercise caution, especially at night.")
        else:
            st.success("✅ This area appears safe for women.")
        
        st.write("ℹ️ Demo score is generated using heuristics. Connect real crime/review/news datasets for production.")
        
    except Exception as e:
        st.error(f"Error fetching safety data: {e}")
