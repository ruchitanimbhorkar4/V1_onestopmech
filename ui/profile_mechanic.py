import streamlit as st
import os
import json

def profile_mechanic_page():
    st.title("Mechanic Profile Setup")
    st.write("Please fill in your mechanic profile information below:")

    full_name = st.text_input("Full Name *")
    email = st.text_input("Email Address *")
    phone_no = st.text_input("Phone Number *")
    city = st.text_input("City *")
    area = st.text_input("Area / Locality *")
    state = st.text_input("State *")
    experience = st.text_input("Years of Experience")
    skills = st.text_input("Skills (comma separated, e.g. Tyre, AC, Battery)")

    offers_routine = st.radio(
        "Do you offer routine services?",
        ("No", "Yes"),
        index=0
    )

    packages = []
    if offers_routine == "Yes":
        st.write("### Routine Service Packages")

        # Initialize package count in session state
        if 'package_count' not in st.session_state:
            st.session_state['package_count'] = 1

        def add_package():
            st.session_state['package_count'] += 1

        st.button("Add Package", on_click=add_package)

        # Collect package details for each package slot
        for i in range(st.session_state['package_count']):
            st.markdown(f"#### Package #{i+1}")
            pkg_name = st.text_input(f"Package Name #{i+1}", key=f"pkg_name_{i}")
            pkg_price = st.number_input(f"Package Price #{i+1}", min_value=0, step=1, key=f"pkg_price_{i}")
            pkg_duration = st.text_input(f"Package Duration #{i+1} (e.g. 1.0 hour)", key=f"pkg_duration_{i}")
            pkg_vehicle = st.text_input(f"Vehicle Type #{i+1}", key=f"pkg_vehicle_{i}")
            pkg_points = st.number_input(f"Inspection Points #{i+1}", min_value=0, step=1, key=f"pkg_points_{i}")

            # Only add packages with a valid name
            if pkg_name.strip():
                packages.append({
                    "name": pkg_name.strip(),
                    "price": pkg_price,
                    "time": pkg_duration.strip(),
                    "vehicle": pkg_vehicle.strip(),
                    "inspection_points": pkg_points
                })

    photo_uploaded = st.file_uploader("Upload Profile Photo (optional)", type=["jpg", "jpeg", "png"])

    if st.button("Save My Profile"):
        # Validate mandatory fields
        required_fields = [full_name, email, phone_no, city, area, state]
        if not all(field.strip() for field in required_fields):
            st.error("Please fill in all required fields marked with *.")
            return

        profile_data = {
            "full_name": full_name.strip(),
            "email": email.strip(),
            "phone_no": phone_no.strip(),
            "city": city.strip(),
            "area": area.strip(),
            "state": state.strip(),
            "experience": experience.strip(),
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "offers_routine_service": (offers_routine == "Yes"),
            "packages": packages if offers_routine == "Yes" else []
        }

        # Save uploaded photo if any
        if photo_uploaded:
            photos_dir = os.path.join("data", "mechanic_photos")
            os.makedirs(photos_dir, exist_ok=True)
            photo_path = os.path.join(photos_dir, f"{email.replace('@','_at_')}.jpg")
            with open(photo_path, "wb") as f:
                f.write(photo_uploaded.getbuffer())
            profile_data["photo"] = photo_path

        profiles_file = os.path.join("data", "mechanic_profiles.json")
        all_profiles = {}
        if os.path.exists(profiles_file):
            with open(profiles_file, "r", encoding="utf-8") as f:
                all_profiles = json.load(f)

        all_profiles[email] = profile_data

        with open(profiles_file, "w", encoding="utf-8") as f:
            json.dump(all_profiles, f, indent=2, ensure_ascii=False)

        st.success("Profile saved! You can now access the mechanic dashboard.")
        st.session_state['mechanic_profile_created'] = True
        st.markdown("---")
        st.info("Fields marked with * are mandatory.")

if __name__ == "__main__":
    profile_mechanic_page()
