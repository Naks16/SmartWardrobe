import streamlit as st
import random

st.set_page_config(page_title="Signup Flow", page_icon="🔐", layout="centered")

# ---------- Custom CSS for dark theme ----------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.pinimg.com/736x/17/b7/26/17b72695ca25bd1405c47c7e6ba400d6.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 40px;
    padding-bottom: 40px;
}

/* Main box */
.block-container {
    background: rgba(0, 0, 0, 0.92);
    padding: 2.5rem 3rem;
    border-radius: 15px;
    box-shadow: 0px 4px 25px rgba(255, 255, 255, 0.15);
    max-width: 650px;
    width: 100%;
    margin: auto;
    color: white;
}

/* Headings & text */
h1, h2, h3, h4, label, p, .stMarkdown {
    color: white !important;
    text-align: center;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid #444;
    padding: 0.4rem;
}

/* --- Selectbox --- */
.stSelectbox div[data-baseweb="select"] {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #444 !important;
    padding: 6px 10px !important;
}
.stSelectbox div[data-baseweb="select"] span {
    color: white !important;
}

/* --- Radio buttons --- */
.stRadio > div {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px;
}
.stRadio div[role="radiogroup"] > label {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 6px 0;
    color: white !important;
    cursor: pointer;
    transition: 0.3s;
}
.stRadio div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: scale(1.02);
}

/* --- Sliders --- */
.stSlider > div {
    padding: 10px 0;
}
.stSlider [role="slider"] {
    background: linear-gradient(90deg, #FF7E5F, #FD3A69) !important;
    border: none !important;
    height: 14px !important;
}
.stSlider [role="slider"]::before {
    background: white !important;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    border: 2px solid #FD3A69;
}
.stSlider .css-14f6p7l, .stSlider label {
    color: white !important;
}

/* --- Buttons (normal + form + nav) --- */
button, [data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, #FF7E5F, #FD3A69) !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    padding: 0.6rem 1rem !important;
    border: none !important;
    transition: 0.2s ease-in-out;
}

button:hover, [data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(90deg, #FD3A69, #FF7E5F) !important;
    transform: scale(1.04);
}
</style>
"""



st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown('<div class="block-container">', unsafe_allow_html=True)

# ---------- Initialize session state ----------
defaults = {
    "page": "otp",
    "otp_sent": False,
    "otp": "",
    "verified": False,
    "profile_saved": False,
    "survey_step": 0,
    "survey_answers": {},
    "phone": "",
    "entered_otp": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- PAGE 1: OTP VERIFICATION ----------
if st.session_state.page == "otp":
    st.title("🔐 Sign Up")
    st.subheader("Step 1: Verify Your Phone")

    with st.form(key="send_otp_form"):
        phone_in = st.text_input("📱 Enter your phone number", key="phone_input")
        send_clicked = st.form_submit_button("Send OTP")
        if send_clicked:
            if phone_in.strip() == "":
                st.error("Please enter a phone number.")
            else:
                st.session_state.phone = phone_in.strip()
                st.session_state.otp = str(random.randint(1000, 9999))
                st.session_state.otp_sent = True
                st.session_state.verified = False
                st.success(f"✅ OTP sent to {st.session_state.phone} (Demo OTP: {st.session_state.otp})")

    if st.session_state.otp_sent:
        st.info(f"OTP has been sent to {st.session_state.phone}.")
        with st.form(key="verify_otp_form"):
            entered = st.text_input("🔑 Enter OTP", key="entered_otp_input")
            verify_clicked = st.form_submit_button("Verify OTP")
            resend_clicked = st.form_submit_button("Resend OTP")

            if verify_clicked:
                st.session_state.entered_otp = entered
                if entered == st.session_state.otp:
                    st.session_state.verified = True
                    st.success("🎉 OTP Verified Successfully!")
                    st.session_state.page = "profile"
                    st.rerun()
                else:
                    st.error("❌ Incorrect OTP. Try again or resend.")

            if resend_clicked:
                st.session_state.otp = str(random.randint(1000, 9999))
                st.session_state.entered_otp = ""
                st.success(f"🔄 New OTP sent (Demo OTP: {st.session_state.otp})")

# ---------- PAGE 2: PROFILE COMPLETION ----------
elif st.session_state.page == "profile":
    st.title("👤 Complete Your Profile")
    st.subheader("Step 2: Tell us about yourself")

    with st.form("profile_form", clear_on_submit=False):
        name = st.text_input("Full Name", key="profile_name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1, key="profile_age")
        profession = st.text_input("Profession", key="profile_prof")
        location = st.text_input("Location", key="profile_loc")
        submitted = st.form_submit_button("Save Profile")

    if submitted:
        if name and profession and location:
            st.session_state.profile_saved = True
            st.success("✅ Profile Saved Successfully!")
            st.session_state.page = "survey_intro"
            st.rerun()
        else:
            st.error("⚠ Please fill all required fields.")

# ---------- PAGE 3A: SURVEY INTRO ----------
elif st.session_state.page == "survey_intro":
    st.title("🧾 Fashion Survey")
    st.write("We’d like to know more about your *fashion sense* to personalize your recommendations.")
    if st.button("Start Survey ➡"):
        st.session_state.survey_step = 0
        st.session_state.page = "survey"
        st.rerun()

# ---------- PAGE 3B: SURVEY ----------
elif st.session_state.page == "survey":
    questions = [
        {"key": "personal_style", "question": "How would you describe your personal style?",
         "type": "multiselect", "options": ["Casual", "Formal", "Sporty", "Boho", "Minimalist", "Mix of everything"]},
        {"key": "mood_influence", "question": "Do you believe your mood influences your outfit choices?",
         "type": "radio", "options": ["Always", "Sometimes", "Rarely"]},
        {"key": "tired_outfit_pref", "question": "When you feel anxious or tired, do you usually prefer muted or expressive outfits?",
         "type": "radio", "options": ["Muted", "Expressive"]},
        {"key": "comfort_importance", "question": "On a scale of 1–10, how important is comfort in your clothing?",
         "type": "slider", "options": [1, 10]},
        {"key": "expression_importance", "question": "On a scale of 1–10, how important is self-expression in your clothing?",
         "type": "slider", "options": [1, 10]},
        {"key": "avoid_outfits", "question": "Do you avoid certain outfits depending on the time of day or place?",
         "type": "radio", "options": ["Yes", "No"]},
        {"key": "safety_compromise", "question": "How often do you compromise your outfit choice for safety reasons?",
         "type": "radio", "options": ["Never", "Sometimes", "Often"]},
        {"key": "daily_influence", "question": "What influences your daily outfit choice the most?",
         "type": "selectbox", "options": ["Mood", "Weather", "Occasion", "People", "Safety", "Other"]},
    ]

    step = st.session_state.survey_step
    q = questions[step]
    st.subheader(f"Q{step+1} of {len(questions)}: {q['question']}")

    form_key = f"survey_form_{step}"
    widget_key = f"ans_{q['key']}"

    with st.form(form_key, clear_on_submit=False):
        if q["type"] == "radio":
            ans = st.radio("", q["options"], key=widget_key)
        elif q["type"] == "multiselect":
            ans = st.multiselect("", q["options"], key=widget_key)
        elif q["type"] == "slider":
            default_val = st.session_state.get(widget_key, (q["options"][0] + q["options"][1]) // 2)
            ans = st.slider("", q["options"][0], q["options"][1], default_val, key=widget_key)
        elif q["type"] == "selectbox":
            prev_val = st.session_state.get(widget_key)
            ans = st.selectbox("", q["options"],
                               index=q["options"].index(prev_val) if prev_val in q["options"] else 0,
                               key=widget_key)
        else:
            ans = st.text_input("", key=widget_key)

        col1, col2 = st.columns([1, 1])
        with col1:
            prev_clicked = st.form_submit_button("⬅ Previous")
        with col2:
            next_clicked = st.form_submit_button("Next ➡")

        st.session_state.survey_answers[q["key"]] = st.session_state.get(widget_key, ans)

        if prev_clicked:
            if step > 0:
                st.session_state.survey_step = step - 1
                st.rerun()

        if next_clicked:
            if step < len(questions) - 1:
                st.session_state.survey_step = step + 1
                st.rerun()
            else:
                st.session_state.page = "survey_done"
                st.rerun()

# ---------- PAGE 4: SURVEY COMPLETE ----------
elif st.session_state.page == "survey_done":
    st.title("🎉 Thank You!")
    st.subheader("You’ve completed the survey.")
    st.success("✅ Your responses have been recorded. We’ll use them to personalize your fashion experience.")
    st.write("Here’s a summary of your answers:")
    st.json(st.session_state.survey_answers)
    if st.button("Finish"):
        st.info("Flow complete. You can now close this page or navigate elsewhere.")

st.markdown("</div>", unsafe_allow_html=True)