import streamlit as st
import random

st.set_page_config(page_title="Signup Flow", page_icon="🔐")

# Initialize session state
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "otp" not in st.session_state:
    st.session_state.otp = None
if "verified" not in st.session_state:
    st.session_state.verified = False

st.title("🔐 Sign Up Page")

# STEP 1: Phone number + OTP verification
if not st.session_state.verified:
    phone = st.text_input("📱 Enter your phone number")

    if st.button("Send OTP"):
        if phone:
            st.session_state.otp = str(random.randint(1000, 9999))  # Generate OTP
            st.session_state.otp_sent = True
            st.success(f"✅ OTP sent to {phone} (Demo OTP: {st.session_state.otp})")
        else:
            st.error("⚠️ Please enter your phone number.")

    if st.session_state.otp_sent:
        entered_otp = st.text_input("🔑 Enter OTP")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verify OTP"):
                if entered_otp == st.session_state.otp:
                    st.session_state.verified = True
                    st.success("🎉 OTP Verified Successfully!")
                else:
                    st.error("❌ Incorrect OTP. Try again.")

        with col2:
            if st.button("Resend OTP"):
                st.session_state.otp = str(random.randint(1000, 9999))
                st.success(f"🔄 New OTP sent (Demo OTP: {st.session_state.otp})")

# STEP 2: Show signup form after verification
if st.session_state.verified:
    st.subheader("👤 Complete Your Profile")
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        profession = st.text_input("Profession")
        location = st.text_input("Location")

        submitted = st.form_submit_button("Sign Up")

    if submitted:
        if name and age and profession and location:
            st.success("✅ Sign Up Successful!")
        else:
            st.error("⚠️ Please fill all fields before signing up.")
