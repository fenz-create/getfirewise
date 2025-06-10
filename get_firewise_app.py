import streamlit as st
import pandas as pd

# Initialize session state for school data
if 'school_data' not in st.session_state:
    st.session_state.school_data = pd.DataFrame(columns=[
        'School Name', 'Programme Stage', 'Next Activity',
        'Contact Person', 'Status', 'Notes'
    ])

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add/Edit School"])

# Dashboard page
if page == "Dashboard":
    st.title("School Programme Dashboard")
    st.write("Manage client relationships and track school progress.")

    # Display the school data table
    st.dataframe(st.session_state.school_data, use_container_width=True)

# Add/Edit School page
elif page == "Add/Edit School":
    st.title("Add or Edit School Entry")

    with st.form("school_form"):
        school_name = st.text_input("School Name")
        programme_stage = st.selectbox("Programme Stage", [
            "Signed Up", "Onboarding", "In Progress", "Completed"
        ])
        next_activity = st.text_input("Next Activity")
        contact_person
