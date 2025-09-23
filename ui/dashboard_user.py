# import streamlit as st
# import os
# import json
# import uuid
# from datetime import datetime



# def load_json(path):
#     if os.path.exists(path):
#         with open(path, 'r', encoding='utf-8') as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return {}
#     return {}


# def load_mechanic_profiles():
#     path = os.path.join('data', 'mechanic_profiles.json')
#     if os.path.exists(path):
#         with open(path, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return {}


# DIY_GUIDES = load_json(os.path.join("data", "DIY_guides.json"))


# def dashboard_user():
#     # Handle quick navigation buttons from dashboard before rendering UI
#     if "navigation_click" in st.session_state:
#         st.session_state['current_page'] = st.session_state['navigation_click']
#         del st.session_state['navigation_click']
#         st.rerun()

#     user_email = st.session_state.get('user_email')
#     full_name = ""

#     if user_email:
#         users = load_json(os.path.join('data', 'users.json'))
#         for user_data in users.values():
#             if user_data.get('email', '').strip().lower() == user_email.strip().lower():
#                 full_name = user_data.get('full_name', "")
#                 break

#     st.title(f"Hello, {full_name}" if full_name else "👤 Welcome User")

#     with st.sidebar:
#         st.title("Menu")

#         # Radio button manages current_page internally
#         selected_page = st.radio(
#             "Navigation",
#             ["Dashboard", "Emergency Repair", "Routine Service", "Repair Request", "DIY", "Profile"],
#             key="current_page"
#         )

#         if st.button("Logout"):
#             for key in list(st.session_state.keys()):
#                 if key.startswith('email') or key.startswith('authenticated') or key.endswith('_authenticated'):
#                     del st.session_state[key]
#             st.session_state['show_login'] = True
#             st.session_state['show_landing'] = True
#             st.rerun()

#     current_page = st.session_state.get('current_page', 'Dashboard')

#     if current_page == "Dashboard":
#         show_dashboard()
#     elif current_page == "Emergency Repair":
#         show_emergency_repair()
#     elif current_page == "Routine Service":
#         show_routine_service()
#     elif current_page == "Repair Request":
#         show_repair_request()
#     elif current_page == "DIY":
#         show_diy()
#     elif current_page == "Profile":
#         show_profile()
#     else:
#         st.error("Page not found.")


# def show_dashboard():
#     st.header("👋 Quick Access")

#     card_titles = [
#         ("🚨 Book Emergency Repair", "Emergency Repair"),
#         ("🛠️ Request Routine Service", "Routine Service"),
#         ("📝 Submit Repair Request", "Repair Request"),
#         ("📚 Access DIY Guides and Tips", "DIY")
#     ]

#     col1, col2 = st.columns(2)

#     for i, (label, page) in enumerate(card_titles):
#         with col1 if i < 2 else col2:
#             card = st.button(label, key=f"card_{page}")
#             st.markdown("""
#                 <style>
#                 div.stButton > button {
#                     width: 100%;
#                     text-align: left;
#                     padding: 16px;
#                     font-size: 1.15rem;
#                     border-radius: 14px;
#                     margin-bottom: 10px;
#                     box-shadow: 0 2px 7px #e5e5e5;
#                     background: #f3f5fa;
#                 }
#                 div.stButton > button:hover {
#                     background-color: #e7f3ff;
#                     color: #214889;
#                 }
#                 </style>
#                 """, unsafe_allow_html=True)
#             if card:
#                 st.session_state['navigation_click'] = page
#                 st.rerun()




# def show_emergency_repair():
#     st.header("🚨 Mechanics near you will arrive within 10 minutes!")
#     area = st.text_input("Enter your area/locality*", help="Specify your neighborhood")
#     city = st.text_input("Enter your city*", help="Specify your city")
#     problem = st.text_input("Describe your problem*", help="E.g. flat tyre, engine failure")

#     if st.button("Find Mechanics"):
#         if not area or not city or not problem:
#             st.error("Please complete all fields!")
#             return

#         mechanics = load_mechanic_profiles()
#         if not mechanics:
#             st.warning("No mechanic profiles available in the system.")
#             return

#         matched = {}
#         area_lower = area.lower().strip()
#         city_lower = city.lower().strip()
#         problem_lower = problem.lower().strip()

#         for email, mech in mechanics.items():
#             skills = [s.lower() for s in mech.get("skills", [])]
#             if mech.get("area", "").lower() == area_lower and mech.get("city", "").lower() == city_lower:
#                 if problem_lower in skills or any(problem_lower in skill for skill in skills):
#                     matched[email] = mech

#         if matched:
#             render_mechanic_cards(matched)
#             return

#         # If no exact area match, try city only
#         city_matches = {}
#         for email, mech in mechanics.items():
#             if mech.get("city", "").lower() == city_lower:
#                 if problem_lower in [s.lower() for s in mech.get("skills", [])]:
#                     city_matches[email] = mech

#         if city_matches:
#             st.warning(f"No exact matches in {area}. Showing city mechanics instead.")
#             render_mechanic_cards(city_matches)
#             return

#         st.error(f"Sorry, no mechanics found in {city}.")



# def show_routine_service():
#     st.header("Routine Service")
#     city = st.text_input("Enter city")
#     if not city:
#         st.info("Enter city")
#         return
#     mechanics = load_mechanic_profiles()
#     filtered = {k:v for k,v in mechanics.items() if v.get('city','').lower() == city.lower() and v.get('offers_routine_service', False)}
#     if not filtered:
#         st.info("No mechanics support routine service in your city")
#         return
#     mech_list = list(filtered.values())
#     mech_keys = list(filtered.keys())
#     mech_names = [f"{m['full_name']} ({m.get('area','')})" for m in mech_list]
#     idx = st.selectbox("Select mechanic", options=range(len(mech_list)), format_func=lambda x: mech_names[x])
#     mechanic = mech_list[idx]
#     mech_id = mech_keys[idx]
#     st.markdown(f"**{mechanic['full_name']}**")
#     packages = mechanic.get('packages', [])
#     if not packages:
#         st.warning("Mechanic has no packages")
#         return
#     if 'selected_pkg_idx' not in st.session_state:
#         st.session_state.selected_pkg_idx = None
#     if 'show_popup' not in st.session_state:
#         st.session_state.show_popup = False
#     cols = st.columns(len(packages))
#     for i, pkg in enumerate(packages):
#         border = 'border: 3px solid #B71C1C;' if st.session_state.selected_pkg_idx == i else ''
#         with cols[i]:
#             st.markdown(f"""
#             <div style="padding: 15px; margin: 5px; background: #ffeff3; border-radius: 15px; box-shadow: 0 4px 10px rgba(183,28,28,0.25); {border}">
#             <h4 style="color:#B71C1C;">{pkg['name']}</h4>
#             <h3 style="margin-top:-10px;">₹{pkg['price']}</h3>
#             <p>{pkg['time']}</p>
#             <p>{pkg['vehicle']}</p>
#             <p>{pkg['inspection_points']} Points</p>
#             </div>
#             """, unsafe_allow_html=True)
#             if st.button("See Checklist", key=f"chk_{i}"):
#                 st.session_state.selected_pkg_idx = i
#                 st.session_state.show_popup = True
#             if st.button("Book Now", key=f"bk_{i}"):
#                 st.session_state.selected_pkg_idx = i
#                 st.session_state.show_popup = False
#     if st.session_state.show_popup and st.session_state.selected_pkg_idx is not None:
#         display_checklist(packages[st.session_state.selected_pkg_idx])
#     if not st.session_state.show_popup and st.session_state.selected_pkg_idx is not None:
#         booking_form(packages[st.session_state.selected_pkg_idx], mech_id, mechanic['full_name'])
        
# def display_checklist(pkg):
#     checklists = {
#         "At-Home Classic Package": [
#             "Engine Oil Replacement", "Brake inspection", "Air Filter Check", "Brake/Clutch Oil Top-up", 
#             "Battery Check", "Chain Sprocket Tightening", "Suspension Check", "12 Point Check"
#         ],
#         "At-Home Premium Package": [
#             "Engine Oil Replacement", "Oil Filter Check", "Spark Plug Check", "Greasing", "Cables check", 
#             "Lights/Switches Checkup", "Tyre air pressure", "Coolant check", "Eco Foam Wash", "15 Point Check"
#         ]
#     }
#     checklist = checklists.get(pkg['name'], ["Details unavailable"])
#     st.markdown("---")
#     st.header(f"{pkg['name']} Checklist")
#     for item in checklist:
#         st.write(f"- {item}")
#     if st.button("Close checklist"):
#         st.session_state.show_popup = False
#         st.session_state.selected_pkg_idx = None




# def booking_form(pkg, mech_id, mech_name):
#     st.markdown("---")
#     st.header(f"Book {pkg['name']}")
#     st.write(f"Price: ₹{pkg['price']}")
#     st.write(f"Duration: {pkg['time']}")
#     st.write(f"Vehicle: {pkg['vehicle']}")
    
#     # Keep date and time inputs if desired
#     pref_date = st.date_input("Preferred date", min_value=datetime.today())
#     pref_time = st.time_input("Preferred time")
    
#     if st.button("Confirm booking"):
#         # Assume logged-in user email is always available
#         user_email = st.session_state.get('user_email')
#         if not user_email:
#             st.warning("User email missing. Please login again.")
#             return
#         if pref_date < datetime.today().date():
#             st.error("Date cannot be in the past")
#             return
        
#         booking_id = uuid.uuid4().hex[:8]
#         booking = {
#             "id": booking_id,
#             "user_email": user_email,
#             "mechanic_id": mech_id,
#             "mechanic_name": mech_name,
#             "package": pkg['name'],
#             "price": pkg['price'],
#             "date": pref_date.strftime("%Y-%m-%d"),
#             "time": pref_time.strftime("%H:%M:%S"),
#             "status": "New"  # Mark as new request
#         }
        
#         bookings_file = "data/routine_service_requests.json"
#         bookings = load_json(bookings_file)
#         bookings[booking_id] = booking
        
#         with open(bookings_file, 'w') as f:
#             json.dump(bookings, f, indent=2)
        
#         st.success("Booking request sent!")
#         st.balloons()  # Optional animation


# def show_repair_request():
#     st.header("🔧 Repair Request - Single Part Repair")

#     vehicles = ["Car", "Bike", "Scooty"]
#     if 'selected_vehicle' not in st.session_state:
#         st.session_state.selected_vehicle = None
#         st.session_state.custom_vehicle = ""

#     cols = st.columns(len(vehicles))
#     for idx, v_type in enumerate(vehicles):
#         with cols[idx]:
#             if st.button(v_type):
#                 st.session_state.selected_vehicle = v_type
#                 st.session_state.custom_vehicle = ""

#     if not st.session_state.selected_vehicle:
#         st.info("Please select a vehicle type.")
#         return

#     vehicle = st.session_state.selected_vehicle

#     parts_by_vehicle = {
#         "Car": ["Headlight", "Brake", "Tire", "Battery", "Windshield", "Other"],
#         "Bike": ["Headlight", "Brake", "Tire", "Chain", "Battery", "Other"],
#         "Scooty": ["Headlight", "Brake", "Tire", "Battery", "Other"],
#     }

#     parts = parts_by_vehicle.get(vehicle, ["Other"])

#     part = st.selectbox("Choose the part to repair:", parts)
#     if part == "Other":
#         part = st.text_input("Please describe the part or issue:")
#     if not part:
#         st.info("Please select or enter the part to repair.")
#         return

#     urgency = st.slider(
#         "Set Urgency Level:",
#         min_value=1, max_value=5, value=3,
#         help="1 = Low urgency, 5 = Emergency"
#     )
#     urgency_labels = {
#         1: "Low urgency 😊",
#         2: "Routine 🕒",
#         3: "Moderate ⚠️",
#         4: "High 🔥",
#         5: "Emergency 🚨"
#     }
#     st.write(f"Urgency: **{urgency_labels[urgency]}**")

#     pref_date = st.date_input("Preferred Appointment Date:", min_value=datetime.today())
#     pref_time = st.time_input("Preferred Appointment Time:", value=datetime.now().time())

#     if st.button("Submit Repair Request"):
#         user_email = st.session_state.get("user_email")
#         if not user_email:
#             st.error("Please login to submit request.")
#             return
#         if not vehicle or not part:
#             st.error("Please complete all fields.")
#             return

#         request_id = uuid.uuid4().hex[:8]
#         request_file = os.path.join("data", "repair_requests.json")
#         requests = load_json(request_file)
#         new_request = {
#             "id": request_id,
#             "user_email": user_email,
#             "vehicle_type": vehicle,
#             "part": part,
#             "urgency": urgency,
#             "urgency_label": urgency_labels[urgency],
#             "preferred_date": pref_date.strftime("%Y-%m-%d"),
#             "preferred_time": pref_time.strftime("%H:%M:%S"),
#             "status": "New",
#             "assigned_mechanic": None
#         }
#         requests[request_id] = new_request
#         with open(request_file, "w") as f:
#             json.dump(requests, f, indent=2)
#         st.success("Repair request submitted successfully!")
#         st.balloons()



# def show_diy():
#     st.header("DIY - Do It Yourself Guides")
#     if not DIY_GUIDES:
#         st.info("No DIY guides found.")
#         return
#     vehicle_types = sorted({g.get("vehicle_type", "Unknown") for g in DIY_GUIDES})
#     vehicle_filter = st.selectbox("Filter by Vehicle Type", options=["All"] + vehicle_types)
#     issues = sorted({g.get("issue", "Unknown") for g in DIY_GUIDES})
#     issue_filter = st.selectbox("Filter by Issue", options=["All"] + issues)

#     filtered_guides = [
#         g for g in DIY_GUIDES
#         if (vehicle_filter == "All" or g.get("vehicle_type") == vehicle_filter) and
#            (issue_filter == "All" or g.get("issue") == issue_filter)
#     ]

#     if not filtered_guides:
#         st.info("No matching DIY guides found.")
#         return

#     for guide in filtered_guides:
#         with st.expander(guide.get("title", "DIY Guide")):
#             st.write(f"Vehicle Type: {guide.get('vehicle_type', 'N/A')}")
#             st.write(f"Issue: {guide.get('issue', 'N/A')}")
#             steps = guide.get("steps", [])
#             if steps:
#                 st.write("### Steps:")
#                 for i, step in enumerate(steps, 1):
#                     st.write(f"{i}. {step}")
#             tools = guide.get("tools", [])
#             if tools:
#                 st.write(f"Tools Needed: {', '.join(tools)}")
#             safety = guide.get("safety_tips", [])
#             if safety:
#                 st.write("Safety Tips:")
#                 for tip in safety:
#                     st.write(f"- {tip}")
#             video = guide.get("video_url", "")
#             if video:
#                 st.video(video)

# def show_profile():
#     st.header("My Profile")
#     tabs = st.tabs(["Edit Profile", "My Requests", "My Reviews", "Routine Service Bookings"])

#     with tabs[0]:
#         edit_profile()

#     with tabs[1]:
#         show_my_requests()

#     with tabs[2]:
#         show_my_reviews()

#     with tabs[3]:
#         show_routine_service_bookings()

# def edit_profile():
#     user_email = st.session_state.get('user_email')
#     if not user_email:
#         st.error("Please login to edit profile.")
#         return

#     users = load_json(os.path.join("data", "users.json"))
#     user_key = None
#     user_data = None

#     for key, data in users.items():
#         if data.get("email") == user_email:
#             user_key = key
#             user_data = data
#             break

#     if user_data is None:
#         st.error("User profile not found.")
#         return

#     full_name = st.text_input("Full Name", value=user_data.get("full_name", ""))
#     contact = st.text_input("Contact Number", value=user_data.get("contact", ""))

#     if st.button("Save Profile"):
#         if not full_name.strip() or not contact.strip():
#             st.error("Full Name and Contact Number cannot be empty.")
#             return
#         users[user_key]["full_name"] = full_name.strip()
#         users[user_key]["contact"] = contact.strip()

#         with open(os.path.join("data", "users.json"), "w") as f:
#             json.dump(users, f, indent=2)
#         st.success("Profile updated successfully!")

# def show_my_requests():
#     st.header("My Service Requests")
#     user_email = st.session_state.get("user_email")
#     if not user_email:
#         st.error("Please login to view requests.")
#         return

#     req_file = os.path.join("data", "repair_requests.json")
#     requests = load_json(req_file)
#     my_requests = [r for r in requests.values() if r.get("user_email") == user_email]

#     if not my_requests:
#         st.info("You have no service requests.")
#         return

#     for r in my_requests:
#         with st.expander(f"{r.get('part','')} ({r.get('status','')})"):
#             st.write(f"Date: {r.get('preferred_date', '')} at {r.get('preferred_time', '')}")
#             st.write(f"Status: {r.get('status','')}")
#             st.write(f"Assigned Mechanic: {r.get('assigned_mechanic', 'Not assigned')}")



# def show_my_reviews():
#     st.header("My Reviews")

#     # Get logged-in user's email from session state
#     user_email = st.session_state.get("user_email")

#     # Load reviews data from file
#     reviews_file = "data/reviews.json"
#     reviews = {}
#     if os.path.exists(reviews_file):
#         with open(reviews_file, "r", encoding="utf-8") as file:
#             try:
#                 reviews = json.load(file)
#             except json.JSONDecodeError:
#                 reviews = {}

#     # Find reviews made by this user
#     my_reviews = []
#     for review_id, review in reviews.items():
#         if review.get("user_email") == user_email:
#             my_reviews.append(review)

#     # If no reviews found, show message
#     if not my_reviews:
#         st.info("You have not submitted any reviews yet.")
#         return

#     # Display each review
#     for review in my_reviews:
#         mechanic = review.get("mechanic_name", "Unknown mechanic")
#         service = review.get("service", "Unknown service")
#         rating = review.get("rating", 0)
#         comment = review.get("comment", "")

#         st.write(f"**Mechanic:** {mechanic}")
#         st.write(f"Service: {service}")

#         # Show stars for rating
#         stars = "⭐" * rating + "☆" * (5 - rating)
#         st.write(f"Rating: {stars}")

#         st.write(f"Comment: {comment}")
#         st.markdown("---")


















# def show_routine_service_bookings():
#     st.header("My Routine Service Bookings")
#     user_email = st.session_state.get("user_email")
#     if not user_email:
#         st.error("Please login to view bookings.")
#         return
#     booking_file = os.path.join('data', 'routine_service_requests.json')
#     bookings = load_json(booking_file)
#     my_bookings = [b for b in bookings.values() if b.get('user_email') == user_email]
#     if not my_bookings:
#         st.info("No routine service bookings found.")
#         return
#     for b in my_bookings:
#         with st.expander(f"{b['package']} with {b['mechanic_name']} on {b['date']}"):
#             st.write(f"Time: {b['time']}")
#             st.write(f"Price: ₹{b['price']}")
#             st.write(f"Status: {b['status']}")





# def render_mechanic_cards(mechanics):
#     for mech in mechanics.values():
#         st.markdown("---")
#         cols = st.columns([1,3])
#         with cols[0]:
#             photo = mech.get('photo')
#             if photo and os.path.exists(photo):
#                 st.image(photo, width=100)
#             else:
#                 st.write('👤 No Photo')
#         with cols[1]:
#             st.write(f"**{mech.get('full_name', 'Unknown')}**")
#             st.write(f"Location: {mech.get('area', '')}, {mech.get('city', '')}")
#             st.write(f"Skills: {', '.join(mech.get('skills', []))}")

# if __name__ == "__main__":
#     dashboard_user()




import streamlit as st
import os
import json
import uuid
from datetime import datetime

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}



def load_mechanic_profiles():
    path = os.path.join('data', 'mechanic_profiles.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}



DIY_GUIDES = load_json(os.path.join("data", "DIY_guides.json"))



def dashboard_user():
    
    css = """
<style>
/* Sidebar Styling - narrower and lighter */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg,#e5f0fc 0%,#f6fbff 100%);
    border-right: 1px solid #d5def8 !important;
    min-width: 220px !important;   /* Reduced width */
    max-width: 220px !important;   /* Limit max width */
    padding-left: 12px !important;
    padding-right: 12px !important;
}

/* Sidebar titles and headings */
.stTitle, .stSidebar h1, .stSidebar h2, .stSidebar h3 {
    color: #193c66 !important;
}

/* Navigation radio button container and label */
.stRadio > div {
    gap: 12px !important;
}
.stRadio>div>label {
    font-size: 1rem !important;  /* Slightly smaller font */
    color: #224173 !important;
}

/* Highlight active radio option with blue */
.stRadio > div [aria-checked="true"] {
    border-left: 4px solid #25476a !important;
    background: #d7e6fd !important;
    color: #183c6e !important;
}

/* Main greeting styling */
h1, .stTitle {
    color: #19243d !important;
    font-family: 'Montserrat', Arial, sans-serif !important;
    font-size: 3.1rem !important;
    font-weight: 800 !important;
    margin-top: 0.7em;
    margin-bottom: 0.7em;
}

/* Quick access card buttons */
div.stButton > button {
    width: 100%;
    text-align: left;
    padding: 20px 24px;
    font-size: 1.2rem;
    border-radius: 18px;
    margin-bottom: 18px;
    background: #f3f8ff;
    color: #203a56;
    border: 1.5px solid #d1e3fa;
    box-shadow: 0 4px 14px #dce6f9;
    transition: background 0.20s, border 0.20s, color 0.15s;
    font-weight: 600;
    letter-spacing: .4px;
}
div.stButton > button:hover {
    background-color: #d7e9fb;
    border: 1.9px solid #25476a;
    color: #203f7c;
    box-shadow: 0 7px 18px #d0e4fc;
}
div.stButton {
    margin-bottom: 5px !important;
}
</style>
"""

    
    # Handle quick navigation buttons from dashboard before rendering UI
    if "navigation_click" in st.session_state:
        st.session_state['current_page'] = st.session_state['navigation_click']
        del st.session_state['navigation_click']
        st.rerun()


    user_email = st.session_state.get('user_email')
    full_name = ""


    if user_email:
        users = load_json(os.path.join('data', 'users.json'))
        for user_data in users.values():
            if user_data.get('email', '').strip().lower() == user_email.strip().lower():
                full_name = user_data.get('full_name', "")
                break


    st.title(f"Hello, {full_name}" if full_name else "👤 Welcome User")


    with st.sidebar:
        st.title("Menu")


        # Radio button manages current_page internally
        selected_page = st.radio(
            "Navigation",
            ["Dashboard", "Emergency Repair", "Routine Service", "Repair Request", "DIY", "Profile"],
            key="current_page"
        )


        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                if key.startswith('email') or key.startswith('authenticated') or key.endswith('_authenticated'):
                    del st.session_state[key]
            st.session_state['show_login'] = True
            st.session_state['show_landing'] = True
            st.rerun()


    current_page = st.session_state.get('current_page', 'Dashboard')


    if current_page == "Dashboard":
        show_dashboard()
    elif current_page == "Emergency Repair":
        show_emergency_repair()
    elif current_page == "Routine Service":
        show_routine_service()
    elif current_page == "Repair Request":
        show_repair_request()
    elif current_page == "DIY":
        show_diy()
    elif current_page == "Profile":
        show_profile()
    else:
        st.error("Page not found.")



def show_dashboard():
    st.header("👋 Quick Access")


    card_titles = [
        ("🚨 Book Emergency Repair", "Emergency Repair"),
        ("🛠️ Request Routine Service", "Routine Service"),
        ("📝 Submit Repair Request", "Repair Request"),
        ("📚 Access DIY Guides and Tips", "DIY")
    ]


    col1, col2 = st.columns(2)


    for i, (label, page) in enumerate(card_titles):
        with col1 if i < 2 else col2:
            card = st.button(label, key=f"card_{page}")
            st.markdown("""
                <style>
                div.stButton > button {
                    width: 100%;
                    text-align: left;
                    padding: 16px;
                    font-size: 1.15rem;
                    border-radius: 14px;
                    margin-bottom: 10px;
                    box-shadow: 0 2px 7px #e5e5e5;
                    background: #f3f5fa;
                }
                div.stButton > button:hover {
                    background-color: #e7f3ff;
                    color: #214889;
                }
                </style>
                """, unsafe_allow_html=True)
            if card:
                st.session_state['navigation_click'] = page
                st.rerun()



def show_emergency_repair():
    st.header("🚨 Mechanics near you will arrive within 10 minutes!")
    area = st.text_input("Enter your area/locality*", help="Specify your neighborhood")
    city = st.text_input("Enter your city*", help="Specify your city")
    problem = st.text_input("Describe your problem*", help="E.g. flat tyre, engine failure")

    if st.button("Find Mechanics"):
        if not area or not city or not problem:
            st.error("Please complete all fields!")
            return

        mechanics = load_mechanic_profiles()
        if not mechanics:
            st.warning("No mechanic profiles available in the system.")
            return

        matched = {}
        area_lower = area.lower().strip()
        city_lower = city.lower().strip()
        problem_lower = problem.lower().strip()

        for email, mech in mechanics.items():
            skills = [s.lower() for s in mech.get("skills", [])]
            if mech.get("area", "").lower() == area_lower and mech.get("city", "").lower() == city_lower:
                if problem_lower in skills or any(problem_lower in skill for skill in skills):
                    matched[email] = mech

        if matched:
            render_mechanic_cards(matched)
            return

        # If no exact area match, try city only
        city_matches = {}
        for email, mech in mechanics.items():
            if mech.get("city", "").lower() == city_lower:
                if problem_lower in [s.lower() for s in mech.get("skills", [])]:
                    city_matches[email] = mech

        if city_matches:
            st.warning(f"No exact matches in {area}. Showing city mechanics instead.")
            render_mechanic_cards(city_matches)
            return

        st.error(f"Sorry, no mechanics found in {city}.")








def show_routine_service():
    st.header("Routine Service")
    city = st.text_input("Enter city")
    if not city:
        st.info("Enter city")
        return
    mechanics = load_mechanic_profiles()
    filtered = {k:v for k,v in mechanics.items() if v.get('city','').lower() == city.lower() and v.get('offers_routine_service', False)}
    if not filtered:
        st.info("No mechanics support routine service in your city")
        return
    mech_list = list(filtered.values())
    mech_keys = list(filtered.keys())
    mech_names = [f"{m['full_name']} ({m.get('area','')})" for m in mech_list]
    idx = st.selectbox("Select mechanic", options=range(len(mech_list)), format_func=lambda x: mech_names[x])
    mechanic = mech_list[idx]
    mech_id = mech_keys[idx]
    st.markdown(f"**{mechanic['full_name']}**")
    packages = mechanic.get('packages', [])
    if not packages:
        st.warning("Mechanic has no packages")
        return
    if 'selected_pkg_idx' not in st.session_state:
        st.session_state.selected_pkg_idx = None
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = False
    cols = st.columns(len(packages))
    for i, pkg in enumerate(packages):
        border = 'border: 3px solid #B71C1C;' if st.session_state.selected_pkg_idx == i else ''
        with cols[i]:
            st.markdown(f"""
            <div style="padding: 15px; margin: 5px; background: #ffeff3; border-radius: 15px; box-shadow: 0 4px 10px rgba(183,28,28,0.25); {border}">
            <h4 style="color:#B71C1C;">{pkg['name']}</h4>
            <h3 style="margin-top:-10px;">₹{pkg['price']}</h3>
            <p>{pkg['time']}</p>
            <p>{pkg['vehicle']}</p>
            <p>{pkg['inspection_points']} Points</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("See Checklist", key=f"chk_{i}"):
                st.session_state.selected_pkg_idx = i
                st.session_state.show_popup = True
            if st.button("Book Now", key=f"bk_{i}"):
                st.session_state.selected_pkg_idx = i
                st.session_state.show_popup = False
    if st.session_state.show_popup and st.session_state.selected_pkg_idx is not None:
        display_checklist(packages[st.session_state.selected_pkg_idx])
    if not st.session_state.show_popup and st.session_state.selected_pkg_idx is not None:
        booking_form(packages[st.session_state.selected_pkg_idx], mech_id, mechanic['full_name'])
        
def display_checklist(pkg):
    checklists = {
        "At-Home Classic Package": [
            "Engine Oil Replacement", "Brake inspection", "Air Filter Check", "Brake/Clutch Oil Top-up", 
            "Battery Check", "Chain Sprocket Tightening", "Suspension Check", "12 Point Check"
        ],
        "At-Home Premium Package": [
            "Engine Oil Replacement", "Oil Filter Check", "Spark Plug Check", "Greasing", "Cables check", 
            "Lights/Switches Checkup", "Tyre air pressure", "Coolant check", "Eco Foam Wash", "15 Point Check"
        ]
    }
    checklist = checklists.get(pkg['name'], ["Details unavailable"])
    st.markdown("---")
    st.header(f"{pkg['name']} Checklist")
    for item in checklist:
        st.write(f"- {item}")
    if st.button("Close checklist"):
        st.session_state.show_popup = False
        st.session_state.selected_pkg_idx = None



def booking_form(pkg, mech_id, mech_name):
    st.markdown("---")
    st.header(f"Book {pkg['name']}")
    st.write(f"Price: ₹{pkg['price']}")
    st.write(f"Duration: {pkg['time']}")
    st.write(f"Vehicle: {pkg['vehicle']}")
    
    # Keep date and time inputs if desired
    pref_date = st.date_input("Preferred date", min_value=datetime.today())
    pref_time = st.time_input("Preferred time")
    
    if st.button("Confirm booking"):
        # Assume logged-in user email is always available
        user_email = st.session_state.get('user_email')
        if not user_email:
            st.warning("User email missing. Please login again.")
            return
        if pref_date < datetime.today().date():
            st.error("Date cannot be in the past")
            return
        
        booking_id = uuid.uuid4().hex[:8]
        booking = {
            "id": booking_id,
            "user_email": user_email,
            "mechanic_id": mech_id,
            "mechanic_name": mech_name,
            "package": pkg['name'],
            "price": pkg['price'],
            "date": pref_date.strftime("%Y-%m-%d"),
            "time": pref_time.strftime("%H:%M:%S"),
            "status": "New"  # Mark as new request
        }
        
        bookings_file = "data/routine_service_requests.json"
        bookings = load_json(bookings_file)
        bookings[booking_id] = booking
        
        with open(bookings_file, 'w') as f:
            json.dump(bookings, f, indent=2)
        
        st.success("Booking request sent!")
        st.balloons()  # Optional animation



def show_repair_request():
    st.header("🔧 Repair Request - Single Part Repair")


    vehicles = ["Car", "Bike", "Scooty"]
    if 'selected_vehicle' not in st.session_state:
        st.session_state.selected_vehicle = None
        st.session_state.custom_vehicle = ""


    cols = st.columns(len(vehicles))
    for idx, v_type in enumerate(vehicles):
        with cols[idx]:
            if st.button(v_type):
                st.session_state.selected_vehicle = v_type
                st.session_state.custom_vehicle = ""


    if not st.session_state.selected_vehicle:
        st.info("Please select a vehicle type.")
        return


    vehicle = st.session_state.selected_vehicle


    parts_by_vehicle = {
        "Car": ["Headlight", "Brake", "Tire", "Battery", "Windshield", "Other"],
        "Bike": ["Headlight", "Brake", "Tire", "Chain", "Battery", "Other"],
        "Scooty": ["Headlight", "Brake", "Tire", "Battery", "Other"],
    }


    parts = parts_by_vehicle.get(vehicle, ["Other"])


    part = st.selectbox("Choose the part to repair:", parts)
    if part == "Other":
        part = st.text_input("Please describe the part or issue:")
    if not part:
        st.info("Please select or enter the part to repair.")
        return


    urgency = st.slider(
        "Set Urgency Level:",
        min_value=1, max_value=5, value=3,
        help="1 = Low urgency, 5 = Emergency"
    )
    urgency_labels = {
        1: "Low urgency 😊",
        2: "Routine 🕒",
        3: "Moderate ⚠️",
        4: "High 🔥",
        5: "Emergency 🚨"
    }
    st.write(f"Urgency: **{urgency_labels[urgency]}**")


    pref_date = st.date_input("Preferred Appointment Date:", min_value=datetime.today())
    pref_time = st.time_input("Preferred Appointment Time:", value=datetime.now().time())


    if st.button("Submit Repair Request"):
        user_email = st.session_state.get("user_email")
        if not user_email:
            st.error("Please login to submit request.")
            return
        if not vehicle or not part:
            st.error("Please complete all fields.")
            return


        request_id = uuid.uuid4().hex[:8]
        request_file = os.path.join("data", "repair_requests.json")
        requests = load_json(request_file)
        new_request = {
            "id": request_id,
            "user_email": user_email,
            "vehicle_type": vehicle,
            "part": part,
            "urgency": urgency,
            "urgency_label": urgency_labels[urgency],
            "preferred_date": pref_date.strftime("%Y-%m-%d"),
            "preferred_time": pref_time.strftime("%H:%M:%S"),
            "status": "New",
            "assigned_mechanic": None
        }
        requests[request_id] = new_request
        with open(request_file, "w") as f:
            json.dump(requests, f, indent=2)
        st.success("Repair request submitted successfully!")
        st.balloons()






def show_diy():
    st.header("DIY - Do It Yourself Guides")
    if not DIY_GUIDES:
        st.info("No DIY guides found.")
        return
    vehicle_types = sorted({g.get("vehicle_type", "Unknown") for g in DIY_GUIDES})
    vehicle_filter = st.selectbox("Filter by Vehicle Type", options=["All"] + vehicle_types)
    issues = sorted({g.get("issue", "Unknown") for g in DIY_GUIDES})
    issue_filter = st.selectbox("Filter by Issue", options=["All"] + issues)

    filtered_guides = [
        g for g in DIY_GUIDES
        if (vehicle_filter == "All" or g.get("vehicle_type") == vehicle_filter) and
           (issue_filter == "All" or g.get("issue") == issue_filter)
    ]

    if not filtered_guides:
        st.info("No matching DIY guides found.")
        return

    for guide in filtered_guides:
        with st.expander(guide.get("title", "DIY Guide")):
            st.write(f"Vehicle Type: {guide.get('vehicle_type', 'N/A')}")
            st.write(f"Issue: {guide.get('issue', 'N/A')}")
            steps = guide.get("steps", [])
            if steps:
                st.write("### Steps:")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. {step}")
            tools = guide.get("tools", [])
            if tools:
                st.write(f"Tools Needed: {', '.join(tools)}")
            safety = guide.get("safety_tips", [])
            if safety:
                st.write("Safety Tips:")
                for tip in safety:
                    st.write(f"- {tip}")
            video = guide.get("video_url", "")
            if video:
                st.video(video)







def show_profile():
    st.header("My Profile")
    tabs = st.tabs(["Edit Profile", "My Requests", "My Reviews", "Routine Service Bookings"])


    with tabs[0]:
        edit_profile()


    with tabs[1]:
        show_my_requests()


    with tabs[2]:
        show_my_reviews()


    with tabs[3]:
        show_routine_service_bookings()



def edit_profile():
    user_email = st.session_state.get('user_email')
    if not user_email:
        st.error("Please login to edit profile.")
        return


    users = load_json(os.path.join("data", "users.json"))
    user_key = None
    user_data = None


    for key, data in users.items():
        if data.get("email") == user_email:
            user_key = key
            user_data = data
            break


    if user_data is None:
        st.error("User profile not found.")
        return


    full_name = st.text_input("Full Name", value=user_data.get("full_name", ""))
    contact = st.text_input("Contact Number", value=user_data.get("contact", ""))


    if st.button("Save Profile"):
        if not full_name.strip() or not contact.strip():
            st.error("Full Name and Contact Number cannot be empty.")
            return
        users[user_key]["full_name"] = full_name.strip()
        users[user_key]["contact"] = contact.strip()


        with open(os.path.join("data", "users.json"), "w") as f:
            json.dump(users, f, indent=2)
        st.success("Profile updated successfully!")



def show_my_requests():
    st.header("My Service Requests")
    user_email = st.session_state.get("user_email")
    if not user_email:
        st.error("Please login to view requests.")
        return


    req_file = os.path.join("data", "repair_requests.json")
    requests = load_json(req_file)
    my_requests = [r for r in requests.values() if r.get("user_email") == user_email]


    if not my_requests:
        st.info("You have no service requests.")
        return


    for r in my_requests:
        with st.expander(f"{r.get('part','')} ({r.get('status','')})"):
            st.write(f"Date: {r.get('preferred_date', '')} at {r.get('preferred_time', '')}")
            st.write(f"Status: {r.get('status','')}")
            st.write(f"Assigned Mechanic: {r.get('assigned_mechanic', 'Not assigned')}")



def show_my_reviews():
    st.header("My Reviews")


    # Get logged-in user's email from session state
    user_email = st.session_state.get("user_email")
    if not user_email:
        st.error("Please login to view and submit reviews.")
        return


    # Load mechanic profiles for review options
    mechanics = load_mechanic_profiles()
    if not mechanics:
        st.info("No mechanics found to review.")
        return


    # Load reviews data from file
    reviews_file = "data/reviews.json"
    reviews = {}
    if os.path.exists(reviews_file):
        with open(reviews_file, "r", encoding="utf-8") as file:
            try:
                reviews = json.load(file)
            except json.JSONDecodeError:
                reviews = {}


    # Find reviews made by this user
    my_reviews = [review for review in reviews.values() if review.get("user_email") == user_email]


    # Display existing reviews
    if my_reviews:
        st.subheader("Your Submitted Reviews")
        for review in my_reviews:
            mechanic = review.get("mechanic_name", "Unknown mechanic")
            service = review.get("service", "Unknown service")
            rating = review.get("rating", 0)
            comment = review.get("comment", "")


            st.write(f"**Mechanic:** {mechanic}")
            st.write(f"Service: {service}")


            # Show stars for rating
            stars = "⭐" * rating + "☆" * (5 - rating)
            st.write(f"Rating: {stars}")


            if comment:
                st.write(f"Comment: {comment}")
            st.markdown("---")
    else:
        st.info("You have not submitted any reviews yet.")


    # ===== Submit a New Review (simple form) =====
    st.markdown("### Submit a New Review")


# Put the inputs inside a form and auto-clear after submit
    with st.form("review_form", clear_on_submit=True):
    # mechanic picker
        mechanic_items = list(mechanics.items())
        mech_display_names = [
            f"{v.get('full_name','Unknown')} ({v.get('area','')}, {v.get('city','')})"
            for _, v in mechanic_items
        ]
        selected_idx = st.selectbox(
            "Select Mechanic to Review",
            options=range(len(mech_display_names)),
            format_func=lambda x: mech_display_names[x]
        )
        selected_mech_key, selected_mech = mechanic_items[selected_idx]


    # basic inputs
        service = st.text_input("Service performed (e.g., Engine repair, Brake replacement)")
        rating = st.slider("Rating", 1, 5, 5)
        comment = st.text_area("Comments (optional)")


    # one submit button for the form
        submitted = st.form_submit_button("Submit Review")


# Handle submit (outside the form block)
    if submitted:
        if not service.strip():
            st.error("Please enter the service performed.")
        else:
        # read existing reviews
            reviews_file = "data/reviews.json"
            reviews = {}
            if os.path.exists(reviews_file):
                try:
                    with open(reviews_file, "r", encoding="utf-8") as f:
                        reviews = json.load(f)
                except json.JSONDecodeError:
                    reviews = {}


        # small duplicate check to avoid accidental double save
            is_dup = False
            for r in reviews.values():
                if (
                    r.get("user_email") == user_email and
                    r.get("mechanic_id") == selected_mech_key and
                    r.get("service", "").strip().lower() == service.strip().lower() and
                    r.get("rating") == rating and
                    r.get("comment", "").strip() == comment.strip()
                ):
                    is_dup = True
                    break


            if is_dup:
                st.info("This review already exists, so it was not added again.")
            else:
            # create and save new review
                review_id = uuid.uuid4().hex[:8]
                new_review = {
                    "id": review_id,
                    "user_email": user_email,
                    "mechanic_id": selected_mech_key,
                    "mechanic_name": selected_mech.get("full_name", "Unknown"),
                    "service": service.strip(),
                    "rating": rating,
                    "comment": comment.strip()
                }
                reviews[review_id] = new_review
                with open(reviews_file, "w", encoding="utf-8") as f:
                    json.dump(reviews, f, indent=2)


                st.success("Review submitted!")
            # form inputs are already cleared because of clear_on_submit=True
            # refresh the page so your review list updates
                st.rerun()




def show_routine_service_bookings():
    st.header("My Routine Service Bookings")
    user_email = st.session_state.get("user_email")
    if not user_email:
        st.error("Please login to view bookings.")
        return
    booking_file = os.path.join('data', 'routine_service_requests.json')
    bookings = load_json(booking_file)
    my_bookings = [b for b in bookings.values() if b.get('user_email') == user_email]
    if not my_bookings:
        st.info("No routine service bookings found.")
        return
    for b in my_bookings:
        with st.expander(f"{b['package']} with {b['mechanic_name']} on {b['date']}"):
            st.write(f"Time: {b['time']}")
            st.write(f"Price: ₹{b['price']}")
            st.write(f"Status: {b['status']}")



def render_mechanic_cards(mechanics):
    # Load reviews to calculate averages
    reviews_file = "data/reviews.json"
    reviews = load_json(reviews_file)

    for email, mech in mechanics.items():
        st.markdown("---")
        cols = st.columns([1,3])
        with cols[0]:
            photo = mech.get('photo')
            if photo and os.path.exists(photo):
                st.image(photo, width=100)
            else:
                st.write('👤 No Photo')
            
            # Calculate average rating for this mechanic
            mech_reviews = [r for r in reviews.values() if r.get("mechanic_id") == email]
            if mech_reviews:
                ratings = [r.get("rating", 0) for r in mech_reviews]
                avg_rating = sum(ratings) / len(ratings)
                stars = "⭐" * int(avg_rating) + "☆" * (5 - int(avg_rating))
                st.write(f"Average Rating: {stars} ({avg_rating:.1f})")
            else:
                st.write("Average Rating: No ratings yet")
                
        with cols[1]:
            st.write(f"**{mech.get('full_name', 'Unknown')}**")
            st.write(f"Location: {mech.get('area', '')}, {mech.get('city', '')}")
            st.write(f"Skills: {', '.join(mech.get('skills', []))}")



if __name__ == "__main__":
    dashboard_user()
