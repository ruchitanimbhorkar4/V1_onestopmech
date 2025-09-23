import streamlit as st
import os
import json
from auth.authentication import authenticate_user_by_username_or_email

def login_page():
    # --- CSS for Centered, Card-Style Form ---
    st.markdown("""
    <style>
        body {
            background-color: #f0f2f5 !important;
        }
        .login-header {
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .login-icon { font-size: 3rem; color: #25476a; }
        .login-title { font-size: 2.5rem; font-weight: 700; color: #25476a; margin-top: 0.5rem; }
        .form-subtitle { text-align: center; color: #4F6B72; margin-bottom: 2rem; }
        .stTextInput input {
            border-radius: 10px !important;
            padding: 12px 15px !important;
            border: 1px solid #d0d0d0 !important;
        }
        .stButton>button { border-radius: 10px !important; font-weight: 600 !important; }
        .st-key-login_btn button { background-color: #25476a !important; color: white !important; }
        .st-key-signup_btn button {
            background-color: transparent !important; color: #25476a !important;
            border: 1px solid #25476a !important;
        }
        .st-key-back_btn_new button {
            width: auto !important; background: #fff !important; color: #25476a !important;
            border: 1px solid #ddd !important; padding: 0.5rem 1rem !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Back Button (Correctly Placed) ---
    nav_cols = st.columns([1, 5])
    with nav_cols[0]:
        if st.button("← 🏠Back to home", key="back_btn_new"):
            st.session_state['show_landing'] = True
            st.session_state['show_login'] = False
            st.rerun()

    st.write("")
    st.write("")

    # --- Centering content with st.columns ---
    _, form_col, _ = st.columns([1, 1.5, 1])
    with form_col:
        with st.container(border=True):
            st.markdown('<div class="login-header"><span class="login-icon">🔐</span><h1 class="login-title">Login</h1></div>', unsafe_allow_html=True)
            st.markdown('<p class="form-subtitle">Please enter your login details</p>', unsafe_allow_html=True)
            
            identifier = st.text_input("Username or Email", placeholder="Enter username or email", label_visibility="collapsed", key="login_user_id")
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed", key="login_pass_id")

            if st.button("Login", use_container_width=True, key="login_btn"):
                if not identifier or not password:
                    st.warning("Please fill all fields.")
                else:
                    # Correct file path
                    users_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')
                    success, user, _ = authenticate_user_by_username_or_email(identifier, password, users_file_path)
                    
                    if not success:
                        st.error("Wrong username/email or password.")
                    else:
                        # Correct logic to set authentication and profile flags
                        st.session_state['user_authenticated'] = (user['role'] == 'user')
                        st.session_state['mechanic_authenticated'] = (user['role'] == 'mechanic')
                        st.session_state['admin_authenticated'] = (user['role'] == 'admin')
                        
                        if user['role'] != 'admin':
                            st.session_state[f"{user['role']}_email"] = user['email']
                        else:
                            st.session_state['admin_username'] = user['username']

                        if user['role'] == 'mechanic':
                            profile_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mechanic_profiles.json')
                            profiles = {}
                            if os.path.exists(profile_file_path) and os.path.getsize(profile_file_path) > 0:
                                with open(profile_file_path, 'r') as f:
                                    profiles = json.load(f)
                            st.session_state['mechanic_profile_created'] = user['email'] in profiles

                        st.session_state['show_login'] = False
                        st.success("Login successful!")
                        st.rerun()

            if st.button("Don't have an account? Signup", use_container_width=True, key="signup_btn"):
                st.session_state['show_signup'] = True
                st.session_state['show_login'] = False
                st.rerun()
