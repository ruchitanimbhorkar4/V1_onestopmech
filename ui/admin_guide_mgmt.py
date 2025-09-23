import streamlit as st
import os
import json

DIY_GUIDES_PATH = os.path.join("data", "diy_guides.json")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def admin_guide_mgmt_page():
    st.title("Admin - Manage DIY Guides")

    # Initialize session variables for form inputs and states
    if "tutorial_added" not in st.session_state:
        st.session_state["tutorial_added"] = False

    if "form_active" not in st.session_state:
        st.session_state["form_active"] = True  # True when form is visible

    # Load existing tutorials
    tutorials = load_json(DIY_GUIDES_PATH)

    if st.session_state["form_active"]:
        # Form input fields
        vehicle_type = st.text_input("Vehicle Type", value=st.session_state.get("vehicle_type", ""))
        issue = st.text_input("Issue", value=st.session_state.get("issue", ""))
        title = st.text_input("Tutorial Title", value=st.session_state.get("title", ""))
        steps_text = st.text_area("Steps (one step per line)", value=st.session_state.get("steps_text", ""))
        tools_text = st.text_input("Tools Needed (comma separated)", value=st.session_state.get("tools_text", ""))
        safety_text = st.text_area("Safety Tips (one per line)", value=st.session_state.get("safety_text", ""))
        video_url = st.text_input("Video URL (YouTube embed link expected)", value=st.session_state.get("video_url", ""))

        # Store inputs back to session_state so they persist during interaction
        st.session_state["vehicle_type"] = vehicle_type
        st.session_state["issue"] = issue
        st.session_state["title"] = title
        st.session_state["steps_text"] = steps_text
        st.session_state["tools_text"] = tools_text
        st.session_state["safety_text"] = safety_text
        st.session_state["video_url"] = video_url

        if st.button("Add Tutorial"):
            if not all([vehicle_type.strip(), issue.strip(), title.strip(), steps_text.strip()]):
                st.error("Please fill Vehicle Type, Issue, Title, and Steps at minimum.")
            else:
                # Check for duplicate tutorial by title, vehicle_type, and issue
                duplicate = False
                for t in tutorials:
                    if (t.get("title", "").lower() == title.strip().lower() and
                        t.get("vehicle_type", "").lower() == vehicle_type.strip().lower() and
                        t.get("issue", "").lower() == issue.strip().lower()):
                        duplicate = True
                        break

                if duplicate:
                    st.error("Tutorial already exists for this vehicle and issue. Please add a different tutorial.")
                else:
                    new_tutorial = {
                        "title": title.strip(),
                        "vehicle_type": vehicle_type.strip(),
                        "issue": issue.strip(),
                        "steps": [step.strip() for step in steps_text.splitlines() if step.strip()],
                        "tools": [tool.strip() for tool in tools_text.split(",") if tool.strip()],
                        "safety_tips": [tip.strip() for tip in safety_text.splitlines() if tip.strip()],
                        "video_url": video_url.strip()
                    }

                    tutorials.append(new_tutorial)
                    save_json(DIY_GUIDES_PATH, tutorials)
                    st.success(f"Added tutorial '{title}' for {vehicle_type} - {issue}.")

                    # Hide form, show add more button
                    st.session_state["form_active"] = False
                    st.session_state["tutorial_added"] = True

    else:
        if st.session_state.get("tutorial_added", False):
            st.info("Tutorial added successfully!")
            st.session_state["tutorial_added"] = False

        if st.button("Add More Tutorials"):
            # Reset form inputs
            keys = ["vehicle_type", "issue", "title", "steps_text", "tools_text", "safety_text", "video_url"]
            for k in keys:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state["form_active"] = True

if __name__ == "__main__":
    admin_guide_mgmt_page()
