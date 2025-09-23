# import streamlit as st
# import ui.admin_guide_mgmt as guide_mgmt

# def manage_user_features_page():
#     st.title("Manage User Features")

#     if "active_user_feature" not in st.session_state:
#         st.session_state["active_user_feature"] = None

#     if st.session_state["active_user_feature"] is None:
#         show_feature_cards()
#     else:
#         if st.button("← Back to Manage User Features"):
#             st.session_state["active_user_feature"] = None
#         st.markdown("---")

#         if st.session_state["active_user_feature"] == "user_accounts":
#             show_user_accounts()
#         elif st.session_state["active_user_feature"] == "diy_guides":
#             guide_mgmt.admin_guide_mgmt_page()
#         elif st.session_state["active_user_feature"] == "user_complaints":
#             show_user_complaints()

# def show_feature_cards():
#     cards = [
#         {
#             "title": "User Accounts",
#             "description": "Manage user accounts including creation, suspension, and deletion.",
#             "key": "user_accounts"
#         },
#         {
#             "title": "DIY Guides",
#             "description": "Add, update, or delete DIY guides to assist users with self-repairs.",
#             "key": "diy_guides"
#         },
#         {
#             "title": "User Complaints",
#             "description": "Review and resolve complaints submitted by users.",
#             "key": "user_complaints"
#         }
#     ]

#     cols = st.columns(2)
#     for i, card in enumerate(cards):
#         with cols[i % 2]:
#             st.markdown(
#                 f"""
#                 <div style="
#                     border: 2px solid #4CAF50; 
#                     border-radius: 15px; 
#                     padding: 30px; 
#                     margin-bottom: 30px; 
#                     background-color: #e8f5e9;
#                     min-height: 220px;
#                     box-shadow: 3px 3px 8px rgba(0,0,0,0.1);
#                     ">
#                     <h2 style="color:#2e7d32;">{card['title']}</h2>
#                     <p style="font-size: 16px; color:#33691e;">{card['description']}</p>
#                 </div>
#                 """, unsafe_allow_html=True
#             )
#             if st.button(f"Manage {card['title']}", key=card["key"]):
#                 st.session_state["active_user_feature"] = card["key"]

# def show_user_accounts():
#     st.header("User Accounts Management")
#     st.write("User account management UI will be here.")

# def show_user_complaints():
#     st.header("User Complaints Management")
#     st.write("User complaints management UI will be here.")




import streamlit as st
import os
import json
import ui.admin_guide_mgmt as guide_mgmt


# file paths
USERS_FILE = os.path.join("data", "users.json")
ROUTINE_REQUESTS_FILE = os.path.join("data", "routine_service_requests.json")
REPAIR_REQUESTS_FILE = os.path.join("data", "repair_requests.json")
REVIEWS_FILE = os.path.join("data", "reviews.json")


def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def manage_user_features_page():
    st.title("Manage User Features")
    if "active_user_feature" not in st.session_state:
        st.session_state["active_user_feature"] = None

    if st.session_state["active_user_feature"] is None:
        show_feature_cards()
    else:
        if st.button("← Back to Manage User Features"):
            st.session_state["active_user_feature"] = None
            st.rerun()
        st.markdown("---")
        if st.session_state["active_user_feature"] == "user_accounts":
            show_user_accounts()
        elif st.session_state["active_user_feature"] == "diy_guides":
            guide_mgmt.admin_guide_mgmt_page()
        # removed: user_complaints branch

def show_feature_cards():
    cards = [
        {
            "title": "User Accounts",
            "description": "Manage user accounts including creation, suspension, and deletion.",
            "key": "user_accounts"
        },
        {
            "title": "DIY Guides",
            "description": "Add, update, or delete DIY guides to assist users with self-repairs.",
            "key": "diy_guides"
        }
        # removed: "User Complaints" card
    ]
    cols = st.columns(2)
    for i, card in enumerate(cards):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #4CAF50; 
                    border-radius: 15px; 
                    padding: 30px; 
                    margin-bottom: 30px; 
                    background-color: #e8f5e9;
                    min-height: 220px;
                    box-shadow: 3px 3px 8px rgba(0,0,0,0.1);
                    ">
                    <h2 style="color:#2e7d32;">{card['title']}</h2>
                    <p style="font-size: 16px; color:#33691e;">{card['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Manage {card['title']}", key=card["key"]):
                st.session_state["active_user_feature"] = card["key"]
                st.rerun()


def show_user_accounts():
    st.header("User Accounts Management")

    users = load_json(USERS_FILE)              # keys are emails
    routine = load_json(ROUTINE_REQUESTS_FILE)
    repair = load_json(REPAIR_REQUESTS_FILE)
    reviews = load_json(REVIEWS_FILE)

    if not users:
        st.info("No users found.")
        return

    # filters
    with st.expander("Filters"):
        name_q = st.text_input("Search by name (optional)", "").strip().lower()
        email_q = st.text_input("Search by email (optional)", "").strip().lower()

    items = list(users.items())  # (email_key, user_data)

    if name_q:
        items = [
            (email_key, data) for email_key, data in items
            if data.get("full_name", "").strip().lower().find(name_q) != -1
        ]
    if email_q:
        items = [
            (email_key, data) for email_key, data in items
            if email_key.strip().lower().find(email_q) != -1
        ]

    if not items:
        st.info("No users match the current filter.")
        return

    for email_key, user in items:
        full_name = user.get("full_name", "Unknown")
        contact = user.get("contact", "")

        # gather stats
        my_routine = [b for b in routine.values() if b.get("user_email") == email_key]
        my_repair = [r for r in repair.values() if r.get("user_email") == email_key]
        my_reviews = [rv for rv in reviews.values() if rv.get("user_email") == email_key]

        total_requests = len(my_routine) + len(my_repair)
        accepted_in_progress = sum(1 for r in my_repair if r.get("status") in ["Accepted", "In Progress"])
        accepted_in_progress += sum(1 for b in my_routine if b.get("status") in ["Accepted", "In Progress"])
        completed = sum(1 for r in my_repair if r.get("status") == "Completed")
        completed += sum(1 for b in my_routine if b.get("status") == "Completed")

        with st.expander(f"{full_name} — {email_key}"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"Name: {full_name}")
                st.write(f"Email: {email_key}")
                st.write(f"Contact: {contact}")
                st.markdown("---")
                st.write("Quick Stats")
                st.write(f"- Total requests: {total_requests}")
                st.write(f"- Accepted/In Progress: {accepted_in_progress}")
                st.write(f"- Completed: {completed}")
                st.write(f"- Routine bookings: {len(my_routine)}")
                st.write(f"- Reviews submitted: {len(my_reviews)}")

                with st.expander("Routine bookings (details)"):
                    if my_routine:
                        for b in sorted(my_routine, key=lambda x: (x.get('date',''), x.get('time','')), reverse=True):
                            st.write(f"{b.get('date','')} {b.get('time','')} | {b.get('package','')} | ₹{b.get('price','')} | {b.get('status','')}")
                    else:
                        st.write("No routine bookings.")

                with st.expander("Repair requests (details)"):
                    if my_repair:
                        for r in sorted(my_repair, key=lambda x: (x.get('preferred_date',''), x.get('preferred_time','')), reverse=True):
                            st.write(f"{r.get('preferred_date','')} {r.get('preferred_time','')} | {r.get('vehicle_type','')} {r.get('part','')} | {r.get('status','')}")
                    else:
                        st.write("No repair requests.")

                with st.expander("Reviews submitted (details)"):
                    if my_reviews:
                        for rv in sorted(my_reviews, key=lambda x: x.get("id",""), reverse=True):
                            rating = int(rv.get("rating", 0)) if str(rv.get("rating","")).isdigit() else 0
                            stars = "⭐" * rating + "☆" * (5 - rating)
                            st.write(f"{stars} | {rv.get('service','')} | {rv.get('comment','')}")
                    else:
                        st.write("No reviews submitted.")

            with col2:
                if st.button("Remove User", key=f"rm_{email_key}"):
                    users.pop(email_key, None)  # remove by email key
                    save_json(USERS_FILE, users)
                    st.success(f"Removed {full_name}")
                    st.rerun()

def show_user_complaints():
    st.header("User Complaints Management")
    st.write("User complaints management UI will be here.")

if __name__ == "__main__":
    manage_user_features_page()
