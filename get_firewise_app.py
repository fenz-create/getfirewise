import streamlit as st
import pandas as pd
import uuid

# Set page layout
st.set_page_config(layout="wide")
st.title("School Engagement Dashboard")

# Top-right add button
top_cols = st.columns([10, 1])
with top_cols[1]:
    if st.button("➕", key="add_school"):
        st.session_state.edit_index = None
        st.session_state.show_form = True

# Initialize session state
if 'school_data' not in st.session_state:
    st.session_state.school_data = pd.DataFrame([
        {
            "School Name": "Greenwood High",
            "Firewise Teacher": "Alice Johnson",
            "Email": "alice@greenwood.edu",
            "Phone": "123-456-7890",
            "Website": "https://greenwood.edu",
            "Stage": "Agreed"
        },
        {
            "School Name": "Maple Leaf Academy",
            "Firewise Teacher": "Brian Smith",
            "Email": "brian@mapleleaf.edu",
            "Phone": "234-567-8901",
            "Website": "https://mapleleaf.edu",
            "Stage": "Agreed"
        },
        {
            "School Name": "Riverdale School",
            "Firewise Teacher": "Catherine Lee",
            "Email": "catherine@riverdale.edu",
            "Phone": "345-678-9012",
            "Website": "https://riverdale.edu",
            "Stage": "Completing"
        },
        {
            "School Name": "Sunrise Elementary",
            "Firewise Teacher": "David Kim",
            "Email": "david@sunrise.edu",
            "Phone": "456-789-0123",
            "Website": "https://sunrise.edu",
            "Stage": "Completing"
        },
        {
            "School Name": "Hilltop School",
            "Firewise Teacher": "Emma Brown",
            "Email": "emma@hilltop.edu",
            "Phone": "567-890-1234",
            "Website": "https://hilltop.edu",
            "Stage": "Firefighter Visit"
        },
        {
            "School Name": "Lakeside Academy",
            "Firewise Teacher": "Frank Green",
            "Email": "frank@lakeside.edu",
            "Phone": "678-901-2345",
            "Website": "https://lakeside.edu",
            "Stage": "Firefighter Visit"
        }
    ])

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# Add or edit school form
def add_or_edit_school_form():
    if not st.session_state.show_form and st.session_state.edit_index is None:
        return

    is_editing = st.session_state.edit_index is not None
    st.subheader("Edit School" if is_editing else "Add New School")

    if is_editing:
        school = st.session_state.school_data.loc[st.session_state.edit_index]
    else:
        school = {}

    with st.form("school_form"):
        name = st.text_input("School Name", value=school.get("School Name", ""))
        teacher = st.text_input("Firewise Teacher Name", value=school.get("Firewise Teacher", ""))
        email = st.text_input("Email", value=school.get("Email", ""))
        phone = st.text_input("Phone Number", value=school.get("Phone", ""))
        website = st.text_input("Website", value=school.get("Website", ""))
        stage = st.selectbox("Stage", ["Agreed", "Completing", "Firefighter Visit"],
                             index=["Agreed", "Completing", "Firefighter Visit"].index(school.get("Stage", "Agreed")))

        submitted = st.form_submit_button("Update" if is_editing else "Add")
        cancel = st.form_submit_button("Cancel")

        if submitted:
            new_entry = {
                "School Name": name,
                "Firewise Teacher": teacher,
                "Email": email,
                "Phone": phone
