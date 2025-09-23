# app.py
import streamlit as st
from datetime import datetime
from ui import (
    landing, 
    login, 
    signup, 
    profile_mechanic, 
    dashboard_user, 
    dashboard_mechanic, 
    dashboard_admin
)

def main():
    if 'current_time' not in st.session_state:
        st.session_state['current_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Hide streamlit menu & footer
    hide_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_style, unsafe_allow_html=True)

    # Initialize all necessary UI flags
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False
    if 'show_landing' not in st.session_state:
        st.session_state['show_landing'] = True

    # Routing for authenticated users
    if st.session_state.get('user_authenticated', False):
        dashboard_user.dashboard_user()
        return

    if st.session_state.get('mechanic_authenticated', False):
        if not st.session_state.get('mechanic_profile_created', False):
            profile_mechanic.profile_mechanic_page()
        else:
            dashboard_mechanic.dashboard_mechanic()
        return

    if st.session_state.get('admin_authenticated', False):
        dashboard_admin.dashboard_admin()
        return

    # Routing for non-authenticated pages
    if st.session_state.get('show_login', False):
        login.login_page()
    elif st.session_state.get('show_signup', False):
        signup.signup_page()
    else:
        # Default fallback to landing page
        landing.landing_page()

def logout():
    """Clear all session auth and UI flags, redirect to landing."""
    auth_keys = ['user_authenticated', 'mechanic_authenticated', 'admin_authenticated']
    info_keys = ['user_email', 'mechanic_email', 'admin_username']
    ui_keys = ['show_login', 'show_signup']
    
    for key in auth_keys:
        st.session_state[key] = False
    for key in info_keys:
        st.session_state[key] = ""
    for key in ui_keys:
        st.session_state[key] = False
        
    st.session_state['show_landing'] = True
    st.session_state['mechanic_profile_created'] = False
    st.rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="ONESTOP|MECH",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
