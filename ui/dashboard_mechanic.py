# import streamlit as st
# import os
# import json
# from streamlit_calendar import calendar

# # File paths
# PROFILE_FILE = os.path.join("data", "mechanic_profiles.json")
# ROUTINE_REQUESTS_FILE = os.path.join("data", "routine_service_requests.json")
# REPAIR_REQUESTS_FILE = os.path.join("data", "repair_requests.json")

# # Load and save helpers
# def load_json_data(filepath):
#     if os.path.exists(filepath):
#         with open(filepath, "r", encoding="utf-8") as f:
#             return json.load(f)
#     return {}

# def save_json_data(filepath, data):
#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

# # Show job requests in two tabs with accept/decline/complete
# def show_job_requests():
#     st.title("Job Requests")
#     tab1, tab2 = st.tabs(["Routine Service", "Repair Requests"])

#     with tab1:
#         st.header("Routine Service Requests")
#         routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
#         show_requests(routine_requests, is_routine=True)

#     with tab2:
#         st.header("Repair Requests")
#         repair_requests = load_json_data(REPAIR_REQUESTS_FILE)
#         show_requests(repair_requests, is_routine=False)

# # Helper to display/manage requests
# def show_requests(all_requests, is_routine):
#     mechanic_email = st.session_state.get("mechanic_email", "")
#     if not mechanic_email:
#         st.error("Mechanic not logged in.")
#         return

#     filtered = []
#     for req_id, req in all_requests.items():
#         status = req.get("status", "New")
#         assigned_mechanic = req.get("mechanic_email") or req.get("assigned_mechanic")
#         if status == "New" or (assigned_mechanic == mechanic_email and status in ["Accepted", "In Progress"]):
#             filtered.append((req_id, req))

#     if not filtered:
#         st.info("No requests available.")
#         return

#     for req_id, req in filtered:
#         with st.expander(f"Request ID: {req_id} - User: {req.get('user_email', 'N/A')}"):
#             if is_routine:
#                 st.write(f"**Package:** {req.get('package', '')}")
#                 st.write(f"**Price:** ₹{req.get('price', '')}")
#                 st.write(f"**Date & Time:** {req.get('date', '')} at {req.get('time', '')}")
#             else:
#                 st.write(f"**Vehicle:** {req.get('vehicle_type', '')}")
#                 st.write(f"**Part:** {req.get('part', '')}")
#                 st.write(f"**Preferred Date & Time:** {req.get('preferred_date', '')} at {req.get('preferred_time', '')}")

#             st.write(f"**Status:** {req.get('status', 'New')}")

#             col1, col2 = st.columns(2)

#             # Buttons for new requests
#             if req.get("status") == "New":
#                 if col1.button("Accept", key=f"accept_{req_id}"):
#                     req["status"] = "Accepted"
#                     if is_routine:
#                         req["mechanic_email"] = mechanic_email
#                     else:
#                         req["assigned_mechanic"] = mechanic_email
#                     all_requests[req_id] = req
#                     filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
#                     save_json_data(filepath, all_requests)
#                     st.success("You accepted the request!")
#                     st.rerun()

#                 if col2.button("Decline", key=f"decline_{req_id}"):
#                     req["status"] = "Declined"
#                     if is_routine:
#                         req["mechanic_email"] = mechanic_email
#                     else:
#                         req["assigned_mechanic"] = mechanic_email
#                     all_requests[req_id] = req
#                     filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
#                     save_json_data(filepath, all_requests)
#                     st.info("You declined the request.")
#                     st.rerun()

#             # Mark complete option
#             elif req.get("status") in ["Accepted", "In Progress"]:
#                 if col1.button("Mark Completed", key=f"complete_{req_id}"):
#                     req["status"] = "Completed"
#                     all_requests[req_id] = req
#                     filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
#                     save_json_data(filepath, all_requests)
#                     st.success("Marked the job as completed!")
#                     st.rerun()

# # Completed Tasks Feature
# def show_completed_tasks():
#     st.title("Completed Tasks")
#     tab1, tab2 = st.tabs(["Routine Service", "Repair Requests"])
#     mechanic_email = st.session_state.get("mechanic_email", "")

#     with tab1:
#         st.header("Completed Routine Service Tasks")
#         routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
#         tasks = []
#         for req_id, req in routine_requests.items():
#             if req.get("mechanic_email") == mechanic_email and req.get("status") == "Completed":
#                 tasks.append(req)
#         if not tasks:
#             st.info("No completed routine service tasks.")
#         else:
#             for req in sorted(tasks, key=lambda x: (x.get('date',''), x.get('time','')), reverse=True):
#                 with st.expander(f"{req.get('package','')} - {req.get('user_email','')}"):
#                     st.write(f"**Package:** {req.get('package','')}")
#                     st.write(f"**User:** {req.get('user_email','')}")
#                     st.write(f"**Price:** ₹{req.get('price','')}")
#                     st.write(f"**Completed at:** {req.get('date','')} {req.get('time','')}")

#     with tab2:
#         st.header("Completed Repair Tasks")
#         repair_requests = load_json_data(REPAIR_REQUESTS_FILE)
#         tasks = []
#         for req_id, req in repair_requests.items():
#             if (req.get("assigned_mechanic") == mechanic_email or req.get("mechanic_email") == mechanic_email) and req.get("status") == "Completed":
#                 tasks.append(req)
#         if not tasks:
#             st.info("No completed repair tasks.")
#         else:
#             for req in sorted(tasks, key=lambda x: (x.get('preferred_date',''), x.get('preferred_time','')), reverse=True):
#                 with st.expander(f"{req.get('vehicle_type','')} {req.get('part','')} - {req.get('user_email','')}"):
#                     st.write(f"**Vehicle:** {req.get('vehicle_type','')}")
#                     st.write(f"**Part:** {req.get('part','')}")
#                     st.write(f"**User:** {req.get('user_email','')}")
#                     st.write(f"**Completed at:** {req.get('preferred_date','')} {req.get('preferred_time','')}")

# # Full calendar view integration
# def show_calendar():
#     st.title("Work Calendar")
#     mechanic_email = st.session_state.get("mechanic_email", "")
#     if not mechanic_email:
#         st.error("Mechanic not logged in.")
#         return

#     routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
#     repair_requests = load_json_data(REPAIR_REQUESTS_FILE)

#     events = []

#     def add_events(requests, service_type, date_key, time_key):
#         for _, req in requests.items():
#             assigned = req.get("mechanic_email") or req.get("assigned_mechanic")
#             if assigned == mechanic_email and req.get("status") in ["Accepted", "In Progress"]:
#                 date = req.get(date_key)
#                 time = req.get(time_key)
#                 if date:
#                     start_datetime = f"{date}T{time if time else '09:00:00'}"
#                     user = req.get("user_email", "User")
#                     task = req.get("package", "") if service_type == "Routine Service" else req.get("part", "")
#                     title = f"{user} - {task}"
#                     events.append({"start": start_datetime, "title": title})

#     add_events(routine_requests, "Routine Service", "date", "time")
#     add_events(repair_requests, "Repair Request", "preferred_date", "preferred_time")

#     if not events:
#         st.info("No accepted jobs scheduled.")
#     else:
#         calendar(events=events)

# # Profile editor page
# def show_profile():
#     st.title("My Profile")

#     mechanic_email = st.session_state.get("mechanic_email", "")
#     if not mechanic_email:
#         st.error("Mechanic not logged in.")
#         return

#     profiles = load_json_data(PROFILE_FILE)
#     profile = profiles.get(mechanic_email, {})

#     full_name = st.text_input("Full Name", profile.get("full_name", ""))
#     phone_no = st.text_input("Phone Number", profile.get("phone_no", ""))
#     city = st.text_input("City", profile.get("city", ""))
#     area = st.text_input("Area / Locality", profile.get("area", ""))
#     state = st.text_input("State", profile.get("state", ""))
#     experience = st.text_input("Years of Experience", profile.get("experience", ""))
#     skills = st.text_input("Skills (comma separated)", ", ".join(profile.get("skills", [])) if isinstance(profile.get("skills", []), list) else profile.get("skills", ""))

#     if st.button("Save Profile"):
#         if not all([full_name.strip(), phone_no.strip(), city.strip(), area.strip(), state.strip()]):
#             st.error("Please fill all required fields.")
#         else:
#             new_profile = {
#                 "full_name": full_name.strip(),
#                 "phone_no": phone_no.strip(),
#                 "city": city.strip(),
#                 "area": area.strip(),
#                 "state": state.strip(),
#                 "experience": experience.strip(),
#                 "skills": [s.strip() for s in skills.split(",") if s.strip()],
#                 "photo": profile.get("photo", ""),
#                 "offers_routine_service": profile.get("offers_routine_service", False),
#                 "packages": profile.get("packages", [])
#             }
#             profiles[mechanic_email] = new_profile
#             save_json_data(PROFILE_FILE, profiles)
#             st.success("Profile updated!")

# # Main dashboard function with improved sidebar single-click navigation
# def dashboard_mechanic():
#     st.set_page_config(page_title="Mechanic Dashboard", page_icon="🔧", layout="wide")
#     st.sidebar.title("ONESTOP|MECH")

#     # Default to Work Calendar on first load
#     if 'sidebar_choice' not in st.session_state:
#         st.session_state['sidebar_choice'] = "Work Calendar"

#     choice = st.sidebar.radio(
#         "Go to:",
#         ["Work Calendar", "Job Requests", "Completed Tasks", "My Profile"],
#         index=["Work Calendar", "Job Requests", "Completed Tasks", "My Profile"].index(
#             st.session_state['sidebar_choice']
#         )
#     )

#     # Trigger rerun on single-click when selection changes
#     if choice != st.session_state['sidebar_choice']:
#         st.session_state['sidebar_choice'] = choice
#         st.rerun()

#     # Show selected page
#     if choice == "Work Calendar":
#         show_calendar()
#     elif choice == "Job Requests":
#         show_job_requests()
#     elif choice == "Completed Tasks":
#         show_completed_tasks()
#     elif choice == "My Profile":
#         show_profile()

#     # Logout button at bottom
#     st.sidebar.markdown("---")
#     if st.sidebar.button("Logout"):
#         for key in ['mechanic_authenticated', 'mechanic_email', 'mechanic_profile_created']:
#             if key in st.session_state:
#                 del st.session_state[key]
#         st.session_state['show_login'] = True
#         st.rerun()
#         return  # Important to return after rerun to avoid double events

# if __name__ == "__main__":
#     if "mechanic_email" not in st.session_state:
#         st.session_state["mechanic_email"] = "vilas@gmail.com"  # Replace with your test email
#     dashboard_mechanic()




import streamlit as st
import os
import json
from streamlit_calendar import calendar

# File paths
PROFILE_FILE = os.path.join("data", "mechanic_profiles.json")
ROUTINE_REQUESTS_FILE = os.path.join("data", "routine_service_requests.json")
REPAIR_REQUESTS_FILE = os.path.join("data", "repair_requests.json")
REVIEWS_FILE = os.path.join("data", "reviews.json")  # added

# Load and save helpers
def load_json_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Show job requests in two tabs with accept/decline/complete
def show_job_requests():
    st.title("Job Requests")
    tab1, tab2 = st.tabs(["Routine Service", "Repair Requests"])
    with tab1:
        st.header("Routine Service Requests")
        routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
        show_requests(routine_requests, is_routine=True)
    with tab2:
        st.header("Repair Requests")
        repair_requests = load_json_data(REPAIR_REQUESTS_FILE)
        show_requests(repair_requests, is_routine=False)

# Helper to display/manage requests
def show_requests(all_requests, is_routine):
    mechanic_email = st.session_state.get("mechanic_email", "")
    if not mechanic_email:
        st.error("Mechanic not logged in.")
        return

    filtered = []
    for req_id, req in all_requests.items():
        status = req.get("status", "New")
        assigned_mechanic = req.get("mechanic_email") or req.get("assigned_mechanic")
        if status == "New" or (assigned_mechanic == mechanic_email and status in ["Accepted", "In Progress"]):
            filtered.append((req_id, req))

    if not filtered:
        st.info("No requests available.")
        return

    for req_id, req in filtered:
        with st.expander(f"Request ID: {req_id} - User: {req.get('user_email', 'N/A')}"):
            if is_routine:
                st.write(f"**Package:** {req.get('package', '')}")
                st.write(f"**Price:** ₹{req.get('price', '')}")
                st.write(f"**Date & Time:** {req.get('date', '')} at {req.get('time', '')}")
            else:
                st.write(f"**Vehicle:** {req.get('vehicle_type', '')}")
                st.write(f"**Part:** {req.get('part', '')}")
                st.write(f"**Preferred Date & Time:** {req.get('preferred_date', '')} at {req.get('preferred_time', '')}")
            st.write(f"**Status:** {req.get('status', 'New')}")

            col1, col2 = st.columns(2)

            # Buttons for new requests
            if req.get("status") == "New":
                if col1.button("Accept", key=f"accept_{req_id}"):
                    req["status"] = "Accepted"
                    if is_routine:
                        req["mechanic_email"] = mechanic_email
                    else:
                        req["assigned_mechanic"] = mechanic_email
                    all_requests[req_id] = req
                    filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
                    save_json_data(filepath, all_requests)
                    st.success("You accepted the request!")
                    st.rerun()

                if col2.button("Decline", key=f"decline_{req_id}"):
                    req["status"] = "Declined"
                    if is_routine:
                        req["mechanic_email"] = mechanic_email
                    else:
                        req["assigned_mechanic"] = mechanic_email
                    all_requests[req_id] = req
                    filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
                    save_json_data(filepath, all_requests)
                    st.info("You declined the request.")
                    st.rerun()

            # Mark complete option
            elif req.get("status") in ["Accepted", "In Progress"]:
                if col1.button("Mark Completed", key=f"complete_{req_id}"):
                    req["status"] = "Completed"
                    all_requests[req_id] = req
                    filepath = ROUTINE_REQUESTS_FILE if is_routine else REPAIR_REQUESTS_FILE
                    save_json_data(filepath, all_requests)
                    st.success("Marked the job as completed!")
                    st.rerun()

# Completed Tasks Feature
def show_completed_tasks():
    st.title("Completed Tasks")
    tab1, tab2 = st.tabs(["Routine Service", "Repair Requests"])
    mechanic_email = st.session_state.get("mechanic_email", "")

    with tab1:
        st.header("Completed Routine Service Tasks")
        routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
        tasks = []
        for req_id, req in routine_requests.items():
            if req.get("mechanic_email") == mechanic_email and req.get("status") == "Completed":
                tasks.append(req)
        if not tasks:
            st.info("No completed routine service tasks.")
        else:
            for req in sorted(tasks, key=lambda x: (x.get('date',''), x.get('time','')), reverse=True):
                with st.expander(f"{req.get('package','')} - {req.get('user_email','')}"):
                    st.write(f"**Package:** {req.get('package','')}")
                    st.write(f"**User:** {req.get('user_email','')}")
                    st.write(f"**Price:** ₹{req.get('price','')}")
                    st.write(f"**Completed at:** {req.get('date','')} {req.get('time','')}")

    with tab2:
        st.header("Completed Repair Tasks")
        repair_requests = load_json_data(REPAIR_REQUESTS_FILE)
        tasks = []
        for req_id, req in repair_requests.items():
            if (req.get("assigned_mechanic") == mechanic_email or req.get("mechanic_email") == mechanic_email) and req.get("status") == "Completed":
                tasks.append(req)
        if not tasks:
            st.info("No completed repair tasks.")
        else:
            for req in sorted(tasks, key=lambda x: (x.get('preferred_date',''), x.get('preferred_time','')), reverse=True):
                with st.expander(f"{req.get('vehicle_type','')} {req.get('part','')} - {req.get('user_email','')}"):
                    st.write(f"**Vehicle:** {req.get('vehicle_type','')}")
                    st.write(f"**Part:** {req.get('part','')}")
                    st.write(f"**User:** {req.get('user_email','')}")
                    st.write(f"**Completed at:** {req.get('preferred_date','')} {req.get('preferred_time','')}")

# Full calendar view integration
def show_calendar():
    st.title("Work Calendar")
    mechanic_email = st.session_state.get("mechanic_email", "")
    if not mechanic_email:
        st.error("Mechanic not logged in.")
        return

    routine_requests = load_json_data(ROUTINE_REQUESTS_FILE)
    repair_requests = load_json_data(REPAIR_REQUESTS_FILE)

    events = []

    def add_events(requests, service_type, date_key, time_key):
        for _, req in requests.items():
            assigned = req.get("mechanic_email") or req.get("assigned_mechanic")
            if assigned == mechanic_email and req.get("status") in ["Accepted", "In Progress"]:
                date = req.get(date_key)
                time = req.get(time_key)
                if date:
                    start_datetime = f"{date}T{time if time else '09:00:00'}"
                    user = req.get("user_email", "User")
                    task = req.get("package", "") if service_type == "Routine Service" else req.get("part", "")
                    title = f"{user} - {task}"
                    events.append({"start": start_datetime, "title": title})

    add_events(routine_requests, "Routine Service", "date", "time")
    add_events(repair_requests, "Repair Request", "preferred_date", "preferred_time")

    if not events:
        st.info("No accepted jobs scheduled.")
    else:
        calendar(events=events)

# Profile editor page split into two tabs
def show_profile():
    st.title("My Profile and Reviews")
    mechanic_email = st.session_state.get("mechanic_email", "")
    if not mechanic_email:
        st.error("Mechanic not logged in.")
        return

    tab1, tab2 = st.tabs(["My Profile", "My Ratings and Reviews"])

    # ---------- Tab 1: My Profile ----------
    with tab1:
        profiles = load_json_data(PROFILE_FILE)
        profile = profiles.get(mechanic_email, {})

        full_name = st.text_input("Full Name", profile.get("full_name", ""))
        phone_no = st.text_input("Phone Number", profile.get("phone_no", ""))
        city = st.text_input("City", profile.get("city", ""))
        area = st.text_input("Area / Locality", profile.get("area", ""))
        state = st.text_input("State", profile.get("state", ""))
        experience = st.text_input("Years of Experience", profile.get("experience", ""))
        skills = st.text_input(
            "Skills (comma separated)",
            ", ".join(profile.get("skills", [])) if isinstance(profile.get("skills", []), list) else profile.get("skills", "")
        )

        if st.button("Save Profile"):
            if not all([full_name.strip(), phone_no.strip(), city.strip(), area.strip(), state.strip()]):
                st.error("Please fill all required fields.")
            else:
                new_profile = {
                    "full_name": full_name.strip(),
                    "phone_no": phone_no.strip(),
                    "city": city.strip(),
                    "area": area.strip(),
                    "state": state.strip(),
                    "experience": experience.strip(),
                    "skills": [s.strip() for s in skills.split(",") if s.strip()],
                    "photo": profile.get("photo", ""),
                    "offers_routine_service": profile.get("offers_routine_service", False),
                    "packages": profile.get("packages", [])
                }
                profiles[mechanic_email] = new_profile
                save_json_data(PROFILE_FILE, profiles)
                st.success("Profile updated!")

    # ---------- Tab 2: My Ratings and Reviews ----------
    with tab2:
        st.subheader("My Ratings and Reviews")

        reviews = load_json_data(REVIEWS_FILE)
        my_reviews = []
        ratings = []

        for _, r in reviews.items():
            if r.get("mechanic_id") == mechanic_email:
                my_reviews.append(r)
                try:
                    ratings.append(int(r.get("rating", 0)))
                except Exception:
                    pass

        if ratings:
            avg = sum(ratings) / len(ratings)
            stars = "⭐" * int(round(avg)) + "☆" * (5 - int(round(avg)))
            st.write(f"Average Rating: {stars} ({avg:.1f}) from {len(ratings)} review(s)")
        else:
            st.write("Average Rating: No ratings yet")

        if my_reviews:
            st.markdown("#### Recent Reviews")
            for r in sorted(my_reviews, key=lambda x: x.get("id", ""), reverse=True):
                user = r.get("user_email", "Unknown")
                rating_val = r.get("rating", 0)
                try:
                    rating = int(rating_val)
                except Exception:
                    rating = 0
                stars_line = "⭐" * rating + "☆" * (5 - rating)
                service = r.get("service", "Service")
                comment = (r.get("comment", "") or "").strip()
                with st.expander(f"{user} — {service} — {stars_line}"):
                    st.write(f"User: {user}")
                    st.write(f"Service: {service}")
                    st.write(f"Rating: {stars_line}")
                    if comment:
                        st.write(f"Comment: {comment}")
        else:
            st.info("No reviews yet.")

# Main dashboard function with improved sidebar single-click navigation
def dashboard_mechanic():
    st.set_page_config(page_title="Mechanic Dashboard", page_icon="🔧", layout="wide")
    st.sidebar.title("ONESTOP|MECH")

    # Default to Work Calendar on first load
    if 'sidebar_choice' not in st.session_state:
        st.session_state['sidebar_choice'] = "Work Calendar"

    # Renamed menu option here:
    menu_options = ["Work Calendar", "Job Requests", "Completed Tasks", "My Profile and Reviews"]

    choice = st.sidebar.radio(
        "Go to:",
        menu_options,
        index=menu_options.index(st.session_state['sidebar_choice']) if st.session_state['sidebar_choice'] in menu_options else 0
    )

    # Trigger rerun on single-click when selection changes
    if choice != st.session_state['sidebar_choice']:
        st.session_state['sidebar_choice'] = choice
        st.rerun()

    # Show selected page
    if choice == "Work Calendar":
        show_calendar()
    elif choice == "Job Requests":
        show_job_requests()
    elif choice == "Completed Tasks":
        show_completed_tasks()
    elif choice == "My Profile and Reviews":
        show_profile()

    # Logout button at bottom
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        for key in ['mechanic_authenticated', 'mechanic_email', 'mechanic_profile_created']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['show_login'] = True
        st.rerun()
        return  # Important to return after rerun to avoid double events

if __name__ == "__main__":
    if "mechanic_email" not in st.session_state:
        st.session_state["mechanic_email"] = "vilas@gmail.com"  # Replace with your test email
    dashboard_mechanic()
