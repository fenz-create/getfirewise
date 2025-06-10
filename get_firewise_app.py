import streamlit as st
import pandas as pd

# Initialize session state for school data with dummy entries
if 'school_data' not in st.session_state:
    st.session_state.school_data = pd.DataFrame([
        {
            'School Name': 'Greenwood High',
            'Programme Stage': 'Signed Up',
            'Next Activity': 'Schedule onboarding call',
            'Contact Person': 'Alice Johnson',
            'Status': 'Active',
            'Notes': 'Excited to start the program.'
        },
        {
            'School Name': 'Maple Leaf Academy',
            'Programme Stage': 'Onboarding',
            'Next Activity': 'Send training materials',
            'Contact Person': 'Brian Smith',
            'Status': 'Pending',
            'Notes': 'Waiting for confirmation on training date.'
        },
        {
            'School Name': 'Riverdale School',
            'Programme Stage': 'In Progress',
            'Next Activity': 'Review mid-term report',
            'Contact Person': 'Catherine Lee',
            'Status': 'Active',
            'Notes': 'Mid-term review scheduled for next week.'
        },
        {
            'School Name': 'Sunrise Elementary',
            'Programme Stage': 'Completed',
            'Next Activity': 'Send completion certificate',
            'Contact Person': 'David Kim',
            'Status': 'Completed',
            'Notes': 'Successfully completed the program.'
        }
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
        contact_person = st.text_input("Contact Person")
        status = st.selectbox("Status", ["Active", "Pending", "Completed"])
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Submit")

        if submitted:
            new_entry = {
                'School Name': school_name,
                'Programme Stage': programme_stage,
                'Next Activity': next_activity,
                'Contact Person': contact_person,
                'Status': status,
                'Notes': notes
            }
            st.session_state.school_data = pd.concat([
                st.session_state.school_data,
                pd.DataFrame([new_entry])
            ], ignore_index=True)
            st.success("School entry added successfully!")
