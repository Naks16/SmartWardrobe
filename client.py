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
import streamlit as st
import random
from twilio.rest import Client

# Twilio credentials
account_sid = "AC61a6284c4d4914933a8ad0eaff251cc8"
auth_token = "6356f6590f4fe023942662d3990cf8ff"
twilio_number = "+12405913729"

client = Client(account_sid, auth_token)

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
    phone = st.text_input("📱 Enter your phone number (e.g. +919876543210)")

    if st.button("Send OTP"):
        if phone:
            st.session_state.otp = str(random.randint(1000, 9999))  # Generate OTP
            st.session_state.otp_sent = True

            try:
                message = client.messages.create(
                    body=f"Your SmartWardrobe OTP is: {st.session_state.otp}",
                    from_=twilio_number,
                    to=phone
                )
                st.success(f"✅ OTP sent to {phone} successfully!")
            except Exception as e:
                st.error(f"⚠️ Failed to send OTP: {e}")
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
                try:
                    client.messages.create(
                        body=f"Your new SmartWardrobe OTP is: {st.session_state.otp}",
                        from_=twilio_number,
                        to=phone
                    )
                    st.success(f"🔄 New OTP sent to {phone}")
                except Exception as e:
                    st.error(f"⚠️ Failed to resend OTP: {e}")

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
