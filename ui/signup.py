# import streamlit as st
# import os
# import json
# from auth.authentication import email_exists, username_exists, hash_password, load_data, save_data
# from auth.validators import validate_email, validate_password, validate_contact

# def signup_page():
#     # --- Custom CSS to match the login page style ---
#     st.markdown("""
#     <style>
#         body { background-color: #f0f2f5 !important; }
#         .signup-header { text-align: center; margin-bottom: 1.5rem; }
#         .signup-icon { font-size: 3rem; color: #25476a; }
#         .signup-title { font-size: 2.5rem; font-weight: 700; color: #25476a; margin-top: 0.5rem; }
#         .form-subtitle { text-align: center; color: #4F6B72; margin-bottom: 1.5rem; }
#         .stTextInput input {
#             border-radius: 10px !important; padding: 12px 15px !important;
#             border: 1px solid #d0d0d0 !important;
#         }
#         .stTextInput label { font-weight: 600; color: #333; }
#         .stRadio [role="radiogroup"] { justify-content: space-around; margin-bottom: 1rem; }
#         .st-key-create_account_btn button { background-color: #25476a !important; color: white !important; }
#         .st-key-back_to_login_btn button {
#             width: auto !important; background: #fff !important; color: #25476a !important;
#             border: 1px solid #ddd !important; padding: 0.5rem 1rem !important;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-radius: 10px !important;
#         }
#     </style>
#     """, unsafe_allow_html=True)
    
#     # --- Back to Login Button ---
#     nav_cols = st.columns([1, 5])
#     with nav_cols[0]:
#         if st.button("← Back to Login", key="back_to_login_btn"):
#             st.session_state['show_signup'] = False
#             st.session_state['show_login'] = True
#             st.rerun()

#     st.write("")
#     st.write("")

#     # --- Centering the form ---
#     _, form_col, _ = st.columns([1, 1.8, 1])
#     with form_col:
#         with st.container(border=True):
#             st.markdown('<div class="signup-header"><span class="signup-icon">📝</span><h1 class="signup-title">Create Account</h1></div>', unsafe_allow_html=True)
#             st.markdown('<p class="form-subtitle">Join our platform to get started</p>', unsafe_allow_html=True)
            
#             st.markdown("<h6>Select Your Role</h6>", unsafe_allow_html=True)
#             role = st.radio("Select Your Role", ["user", "mechanic", "admin"], horizontal=True, label_visibility="collapsed")
            
#             if role == "user": st.info("👤 As a user, you can find and book mechanics.")
#             elif role == "mechanic": st.info("🔧 As a mechanic, you can offer your services.")
#             elif role == "admin": st.info("⚙️ As an admin, you can manage the platform.")
#             st.write("---")
            
#             full_name = st.text_input("Full Name*", placeholder="Enter your full name")
#             username = st.text_input("Username*", placeholder="Choose a unique username")
#             email = st.text_input("Email*", placeholder="Enter your email address")
#             password = st.text_input("Password*", type="password", placeholder="Create a strong password")
#             contact = st.text_input("Contact*", placeholder="Enter your phone number")
#             st.write("")

#             if st.button("Create Account", use_container_width=True, key="create_account_btn"):
#                 # --- THIS IS THE FIX ---
#                 # The path is corrected to go up one directory first (../)
#                 users_file_path = os.path.join('..', 'data', 'users.json')

#                 if not all([full_name, username, email, password, contact]): st.warning("Please fill all required fields.")
#                 elif not validate_email(email): st.error("Please enter a valid email address.")
#                 elif email_exists(email, users_file_path): st.error("This email is already registered.")
#                 elif username_exists(username, users_file_path): st.error("This username is already taken.")
#                 elif not validate_password(password): st.error("Password must be 8+ characters and include uppercase, lowercase, a digit, and a symbol.")
#                 elif not validate_contact(contact): st.error("Contact number must contain 7 to 15 digits only.")
#                 else:
#                     hashed_pwd = hash_password(password)
#                     success = save_user_with_username_fullname(username, email, hashed_pwd, contact, role, full_name, users_file_path)
#                     if success:
#                         st.success("Account created successfully! Please log in.")
#                         st.session_state['show_signup'] = False
#                         st.session_state['show_login'] = True
#                         st.rerun()
#                     else: st.error("An unexpected error occurred. Please try again.")

# def save_user_with_username_fullname(username, email, hashed_password, contact, role, full_name, filename):
#     try:
#         users = load_data(filename)
#         users[username] = {
#             "username": username, "full_name": full_name, "email": email,
#             "password": hashed_password, "contact": contact, "role": role, "status": "Active"
#         }
#         save_data(filename, users)
#         return True
#     except Exception as e:
#         print(f"Error saving user: {e}")
#         return False








import streamlit as st
import os
import json
from auth.authentication import email_exists, username_exists, hash_password
from auth.validators import validate_email, validate_password, validate_contact

def save_user(username, full_name, email, hashed_password, contact, role, filename):
    """
    Safely saves a new user to the JSON file. Creates the directory and file if they don't exist.
    """
    try:
        # Ensure the 'data' directory exists
        data_dir = os.path.dirname(filename)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Load existing users, or initialize an empty dict if the file is missing/empty/corrupt
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = {}  # Treat corrupt file as empty
        else:
            users = {}

        # Add the new user's data
        users[username] = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": hashed_password,
            "contact": contact,
            "role": role,
            "status": "Active"
        }

        # Write the updated dictionary back to the file
        with open(filename, 'w') as f:
            json.dump(users, f, indent=4)
        
        return True
    except Exception as e:
        st.error(f"Error saving user data: {e}")
        return False

def signup_page():
    # --- Custom CSS and Back Button (no changes here) ---
    st.markdown("""
        <style>
            /* Your existing CSS styles */
        </style>
    """, unsafe_allow_html=True)

    nav_cols = st.columns([1, 5])
    with nav_cols[0]:
        if st.button("← Back to Login", key="back_to_login_btn"):
            st.session_state['show_signup'] = False
            st.session_state['show_login'] = True
            st.rerun()

    _, form_col, _ = st.columns([1, 1.8, 1])
    with form_col:
        with st.container(border=True):
            st.markdown('<div class="signup-header"><span class="signup-icon">🔧</span><h1 class="signup-title">Create Account</h1></div>', unsafe_allow_html=True)
            st.markdown('<p class="form-subtitle">Join our platform to get started</p>', unsafe_allow_html=True)
            
            role = st.radio("Select Your Role", ('user', 'mechanic', 'admin'), horizontal=True)

            st.write("---")
            
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a unique username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            contact = st.text_input("Contact", placeholder="Enter your phone number")
            
            st.write("") 

            if st.button("Create Account", use_container_width=True, key="create_account_btn"):
                users_filepath = os.path.join('data', 'users.json')
                
                # --- Validation Checks (no changes here) ---
                if not all([full_name, username, email, password, contact]):
                    st.warning("Please fill all required fields.")
                elif not validate_email(email):
                    st.error("Please enter a valid email address.")
                elif email_exists(email, users_filepath):
                    st.error("This email is already registered.")
                elif username_exists(username, users_filepath):
                    st.error("This username is already taken.")
                elif not validate_password(password):
                    st.error("Password must be 8+ characters and include uppercase, lowercase, a digit, and a symbol.")
                elif not validate_contact(contact):
                    st.error("Contact number must contain 7 to 15 digits only.")
                else:
                    hashed_pwd = hash_password(password)
                    success = save_user(username, full_name, email, hashed_pwd, contact, role, users_filepath)
                    
                    if success:
                        if role == 'mechanic':
                            st.success("Account created! Redirecting to profile setup...")
                            st.session_state['mechanic_authenticated'] = True
                            st.session_state['mechanic_email'] = email
                            st.session_state['mechanic_profile_created'] = False
                            st.session_state['show_signup'] = False
                            st.rerun()
                        else:
                            st.success("Account created successfully! Please log in.")
                            st.session_state['show_signup'] = False
                            st.session_state['show_login'] = True
                            st.rerun()
                    # The else block for the "unexpected error" is now handled inside save_user
