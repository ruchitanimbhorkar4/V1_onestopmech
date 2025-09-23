# import streamlit as st

# def manage_mechanic_features_page():
#     st.title("Manage Mechanic Features")

#     if "active_mechanic_feature" not in st.session_state:
#         st.session_state["active_mechanic_feature"] = None

#     if st.session_state["active_mechanic_feature"] is None:
#         show_feature_cards()
#     else:
#         if st.button("← Back to Manage Mechanic Features"):
#             st.session_state["active_mechanic_feature"] = None
#         st.markdown("---")

#         if st.session_state["active_mechanic_feature"] == "mechanic_accounts":
#             show_mechanic_accounts()
#         elif st.session_state["active_mechanic_feature"] == "mechanic_ratings":
#             show_mechanic_ratings()

# def show_feature_cards():
#     cards = [
#         {
#             "title": "Mechanic Accounts",
#             "description": "Manage mechanic profiles including registration approval, suspension, and updates.",
#             "key": "mechanic_accounts"
#         },
#         {
#             "title": "Mechanic Ratings",
#             "description": "View and moderate mechanic ratings and customer reviews to maintain quality.",
#             "key": "mechanic_ratings"
#         }
#     ]

#     cols = st.columns(2)
#     for i, card in enumerate(cards):
#         with cols[i % 2]:
#             st.markdown(
#                 f"""
#                 <div style="
#                     border: 2px solid #1976d2; 
#                     border-radius: 15px; 
#                     padding: 30px; 
#                     margin-bottom: 30px; 
#                     background-color: #e3f2fd;
#                     min-height: 220px;
#                     box-shadow: 3px 3px 8px rgba(0,0,0,0.1);
#                     ">
#                     <h2 style="color:#0d47a1;">{card['title']}</h2>
#                     <p style="font-size: 16px; color:#1565c0;">{card['description']}</p>
#                 </div>
#                 """, unsafe_allow_html=True
#             )
#             if st.button(f"Manage {card['title']}", key=card["key"]):
#                 st.session_state["active_mechanic_feature"] = card["key"]

# def show_mechanic_accounts():
#     st.header("Mechanic Accounts Management")
#     st.write("Mechanic account management UI will be here.")

# def show_mechanic_ratings():
#     st.header("Mechanic Ratings Management")
#     st.write("Mechanic ratings management UI will be here.")



import streamlit as st
import os
import json
from streamlit_calendar import calendar

# ---- Files ----
PROFILE_FILE = os.path.join("data", "mechanic_profiles.json")
ROUTINE_REQUESTS_FILE = os.path.join("data", "routine_service_requests.json")
REPAIR_REQUESTS_FILE = os.path.join("data", "repair_requests.json")
REVIEWS_FILE = os.path.join("data", "reviews.json")

# ---- Helpers ----
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

# ---- Main Page Switcher ----
def manage_mechanic_features_page():
    st.title("Manage Mechanic Features")

    if "active_mechanic_feature" not in st.session_state:
        st.session_state["active_mechanic_feature"] = None

    if st.session_state["active_mechanic_feature"] is None:
        show_feature_cards()
    else:
        if st.button("← Back to Manage Mechanic Features"):
            st.session_state["active_mechanic_feature"] = None
            st.rerun()

        st.markdown("---")
        if st.session_state["active_mechanic_feature"] == "mechanic_accounts":
            show_mechanic_accounts()
        elif st.session_state["active_mechanic_feature"] == "mechanic_ratings":
            show_mechanic_ratings()

# ---- Feature Cards ----
def show_feature_cards():
    cards = [
        {
            "title": "Mechanic Accounts",
            "description": "Manage mechanic profiles including registration approval, suspension, and updates.",
            "key": "mechanic_accounts"
        },
        {
            "title": "Mechanic Ratings",
            "description": "View and moderate mechanic ratings and customer reviews to maintain quality.",
            "key": "mechanic_ratings"
        }
    ]
    cols = st.columns(2)
    for i, card in enumerate(cards):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #1976d2; 
                    border-radius: 15px; 
                    padding: 30px; 
                    margin-bottom: 30px; 
                    background-color: #e3f2fd;
                    min-height: 220px;
                    box-shadow: 3px 3px 8px rgba(0,0,0,0.1);
                    ">
                    <h2 style="color:#0d47a1;">{card['title']}</h2>
                    <p style="font-size: 16px; color:#1565c0;">{card['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Manage {card['title']}", key=card["key"]):
                st.session_state["active_mechanic_feature"] = card["key"]
                st.rerun()

# ---- Mechanic Accounts Management ----
def show_mechanic_accounts():
    st.header("Mechanic Accounts Management")

    profiles = load_json(PROFILE_FILE)
    routine = load_json(ROUTINE_REQUESTS_FILE)
    repair = load_json(REPAIR_REQUESTS_FILE)
    reviews = load_json(REVIEWS_FILE)

    if not profiles:
        st.info("No mechanics found.")
        return

    # Optional filters
    with st.expander("Filters"):
        city_filter = st.text_input("Filter by city (optional)", "")
        skill_filter = st.text_input("Filter by skill keyword (optional)", "")

    mechanic_items = list(profiles.items())

    # Apply simple filters
    if city_filter.strip():
        mechanic_items = [
            (email, m) for email, m in mechanic_items
            if m.get("city", "").strip().lower() == city_filter.strip().lower()
        ]
    if skill_filter.strip():
        key = skill_filter.strip().lower()
        mechanic_items = [
            (email, m) for email, m in mechanic_items
            if any(key in s.lower() for s in (m.get("skills", []) if isinstance(m.get("skills", []), list) else []))
        ]

    if not mechanic_items:
        st.info("No mechanics match the current filter.")
        return

    # List mechanics
    for mech_email, mech in mechanic_items:
        full_name = mech.get("full_name", "Unknown")
        area = mech.get("area", "")
        city = mech.get("city", "")
        skills = mech.get("skills", [])
        photo = mech.get("photo", "")

        # Compute basic stats
        # Routine jobs (accepted/in progress/completed) assigned via mechanic_email
        routine_assigned = [
            r for r in routine.values()
            if r.get("mechanic_email") == mech_email
        ]
        routine_accepted = sum(1 for r in routine_assigned if r.get("status") in ["Accepted", "In Progress"])
        routine_completed = sum(1 for r in routine_assigned if r.get("status") == "Completed")

        # Repair jobs may be stored with assigned_mechanic or mechanic_email
        repair_assigned = [
            r for r in repair.values()
            if r.get("assigned_mechanic") == mech_email or r.get("mechanic_email") == mech_email
        ]
        repair_accepted = sum(1 for r in repair_assigned if r.get("status") in ["Accepted", "In Progress"])
        repair_completed = sum(1 for r in repair_assigned if r.get("status") == "Completed")

        # Reviews for this mechanic (match mechanic_id to email used as key)
        mech_reviews = [rv for rv in reviews.values() if rv.get("mechanic_id") == mech_email]
        ratings = [int(rv.get("rating", 0)) for rv in mech_reviews if isinstance(rv.get("rating", 0), (int, float, str))]
        try:
            ratings = [int(x) for x in ratings]
        except Exception:
            ratings = []
        avg_rating = (sum(ratings) / len(ratings)) if ratings else None
        stars = ("⭐" * int(round(avg_rating)) + "☆" * (5 - int(round(avg_rating)))) if avg_rating is not None else "No ratings yet"

        # Card-like expander per mechanic
        with st.expander(f"{full_name} ({area}, {city}) — {mech_email}"):
            c1, c2 = st.columns([1, 3])
            with c1:
                if photo and os.path.exists(photo):
                    st.image(photo, width=120)
                else:
                    st.write("👤 No Photo")

                # Remove mechanic action
                if st.button("Remove Mechanic", key=f"rm_{mech_email}"):
                    # Delete from profiles and save
                    profiles.pop(mech_email, None)
                    save_json(PROFILE_FILE, profiles)
                    st.success(f"Removed {full_name}")
                    st.rerun()

            with c2:
                st.write(f"Name: {full_name}")
                st.write(f"City/Area: {city} / {area}")
                st.write(f"Skills: {', '.join(skills) if isinstance(skills, list) else skills}")
                st.write(f"Average Rating: {stars} {(f'({avg_rating:.1f})' if avg_rating is not None else '')}")
                st.markdown("---")
                st.write("Summary")
                st.write(f"- Routine: accepted/in-progress = {routine_accepted}, completed = {routine_completed}")
                st.write(f"- Repair: accepted/in-progress = {repair_accepted}, completed = {repair_completed}")
                st.write(f"- Total Reviews: {len(mech_reviews)}")

                # Optional detail breakdowns
                with st.expander("Routine jobs (details)"):
                    if routine_assigned:
                        for r in sorted(routine_assigned, key=lambda x: (x.get("date",""), x.get("time","")), reverse=True):
                            st.write(f"{r.get('date','')} {r.get('time','')} | {r.get('package','')} | ₹{r.get('price','')} | {r.get('status','')}")
                    else:
                        st.write("No routine jobs.")

                with st.expander("Repair jobs (details)"):
                    if repair_assigned:
                        for r in sorted(repair_assigned, key=lambda x: (x.get("preferred_date",""), x.get("preferred_time","")), reverse=True):
                            st.write(f"{r.get('preferred_date','')} {r.get('preferred_time','')} | {r.get('vehicle_type','')} {r.get('part','')} | {r.get('status','')}")
                    else:
                        st.write("No repair jobs.")

                with st.expander("Reviews (details)"):
                    if mech_reviews:
                        for rv in sorted(mech_reviews, key=lambda x: x.get("id",""), reverse=True):
                            rating = int(rv.get("rating", 0)) if str(rv.get("rating","")).isdigit() else 0
                            star_line = "⭐" * rating + "☆" * (5 - rating)
                            st.write(f"{rv.get('user_email','unknown')} | {star_line} | {rv.get('service','')} | {rv.get('comment','')}")
                    else:
                        st.write("No reviews yet.")

# ---- Mechanic Ratings (placeholder or moderation UI) ----
# def show_mechanic_ratings():
#     st.header("Mechanic Ratings Management")
#     st.write("Mechanic ratings management UI will be here.")

def show_mechanic_ratings():
    st.header("Mechanic Ratings")

    profiles = load_json(PROFILE_FILE)                  # mechanics by email key
    reviews = load_json(REVIEWS_FILE) if os.path.exists(REVIEWS_FILE) else {}

    if not profiles:
        st.info("No mechanics found.")
        return

    # simple search
    with st.expander("Filters"):
        name_q = st.text_input("Search by mechanic name (optional)", "").strip().lower()
        city_q = st.text_input("Search by city (optional)", "").strip().lower()

    mech_items = list(profiles.items())

    if name_q:
        mech_items = [
            (email, m) for email, m in mech_items
            if m.get("full_name", "").strip().lower().find(name_q) != -1
        ]
    if city_q:
        mech_items = [
            (email, m) for email, m in mech_items
            if m.get("city", "").strip().lower().find(city_q) != -1
        ]

    if not mech_items:
        st.info("No mechanics match the current filter.")
        return

    for mech_email, mech in mech_items:
        full_name = mech.get("full_name", "Unknown")
        area = mech.get("area", "")
        city = mech.get("city", "")
        photo = mech.get("photo", "")

        # collect this mechanic's reviews
        mech_reviews = [rv for rv in reviews.values() if rv.get("mechanic_id") == mech_email]
        ratings_raw = [rv.get("rating", 0) for rv in mech_reviews]
        ratings = []
        for r in ratings_raw:
            try:
                ratings.append(int(r))
            except Exception:
                pass

        total_reviews = len(ratings)
        avg = (sum(ratings) / total_reviews) if total_reviews > 0 else None
        stars = "No ratings yet" if avg is None else ("⭐" * int(round(avg)) + "☆" * (5 - int(round(avg))))

        with st.expander(f"{full_name} ({area}, {city}) — {mech_email}"):
            c1, c2 = st.columns([1, 3])
            with c1:
                if photo and os.path.exists(photo):
                    st.image(photo, width=120)
                else:
                    st.write("👤 No Photo")
            with c2:
                if avg is None:
                    st.write("Average Rating: No ratings yet")
                else:
                    st.write(f"Average Rating: {stars} ({avg:.1f}) from {total_reviews} review(s)")

                # show all reviews
                if mech_reviews:
                    st.markdown("#### Reviews")
                    for rv in sorted(mech_reviews, key=lambda x: x.get("id", ""), reverse=True):
                        user_email = rv.get("user_email", "Unknown")
                        try:
                            r_val = int(rv.get("rating", 0))
                        except Exception:
                            r_val = 0
                        star_line = "⭐" * r_val + "☆" * (5 - r_val)
                        service = rv.get("service", "Service")
                        comment = (rv.get("comment", "") or "").strip()
                        with st.expander(f"{user_email} — {service} — {star_line}"):
                            st.write(f"User: {user_email}")
                            st.write(f"Service: {service}")
                            st.write(f"Rating: {star_line}")
                            if comment:
                                st.write(f"Comment: {comment}")
                else:
                    st.info("No reviews for this mechanic yet.")

    # You can extend this to list all reviews for moderation.

# ---- Entry Point for this module ----
if __name__ == "__main__":
    manage_mechanic_features_page()
