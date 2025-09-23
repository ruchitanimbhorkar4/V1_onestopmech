import streamlit as st
import ui.admin_user_mgmt as user_mgmt
import ui.admin_mechanic_mgmt as mechanic_mgmt

def dashboard_admin():
    st.sidebar.title("Admin Panel")
    page = st.sidebar.radio("Navigate", ["Dashboard", "Manage Features"])

    if st.sidebar.button("Logout"):
        for key in ['admin_authenticated', 'admin_username']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['show_login'] = True
        st.sidebar.success("Logged out successfully. Please refresh the page.")

    if page == "Dashboard":
        show_admin_home()
    elif page == "Manage Features":
        feature_type = st.sidebar.selectbox("Select Feature Type", ["Manage User Features", "Manage Mechanic Features"])

        if feature_type == "Manage User Features":
            user_mgmt.manage_user_features_page()
        elif feature_type == "Manage Mechanic Features":
            mechanic_mgmt.manage_mechanic_features_page()

def show_admin_home():
    st.title("⚙️ Admin Dashboard")
    if 'admin_username' in st.session_state:
        st.write(f"Welcome: {st.session_state['admin_username']}")

