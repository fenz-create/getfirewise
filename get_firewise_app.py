
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Get Firewise School Engagement Tracker", layout="wide")

st.title("🔥 Get Firewise - School Engagement Tracker Hadlee is awesome!")

# Initialize session state for school data
if "school_data" not in st.session_state:
    st.session_state.school_data = []

# Sidebar for admin view
st.sidebar.header("Admin Dashboard")
if st.sidebar.checkbox("Show Registered Schools"):
    if st.session_state.school_data:
        df = pd.DataFrame(st.session_state.school_data)
        st.sidebar.dataframe(df)
    else:
        st.sidebar.info("No schools registered yet.")

# School Registration Form
st.header("🏫 School Sign-Up")
with st.form("school_form"):
    school_name = st.text_input("School Name")
    contact_name = st.text_input("Contact Person")
    email = st.text_input("Email Address")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central"])
    year_level = st.selectbox("Year Level", ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"])
    agreed = st.checkbox("We agree to participate in the Get Firewise programme.")

    submitted = st.form_submit_button("Register School")
    if submitted:
        if school_name and contact_name and email and agreed:
            st.session_state.school_data.append({
                "School": school_name,
                "Contact": contact_name,
                "Email": email,
                "Region": region,
                "Year Level": year_level,
                "Agreed": "Yes" if agreed else "No",
                "Completed": "No",
                "Visit Booked": "No",
                "Visit Date": ""
            })
            st.success(f"{school_name} has been registered successfully!")
        else:
            st.error("Please complete all required fields and agree to participate.")

# Programme Completion
st.header("✅ Mark Programme Completion")
school_list = [s["School"] for s in st.session_state.school_data]
if school_list:
    selected_school = st.selectbox("Select your school", school_list, key="completion_school")
    if st.button("Mark as Completed"):
        for s in st.session_state.school_data:
            if s["School"] == selected_school:
                s["Completed"] = "Yes"
                st.success(f"{selected_school} marked as completed.")
else:
    st.info("No schools registered yet.")

# Firefighter Visit Booking
st.header("🚒 Book a Firefighter Visit")
if school_list:
    selected_school = st.selectbox("Select your school", school_list, key="visit_school")
    visit_date = st.date_input("Preferred Visit Date", min_value=date.today())
    if st.button("Book Visit"):
        for s in st.session_state.school_data:
            if s["School"] == selected_school:
                if s["Completed"] == "Yes":
                    s["Visit Booked"] = "Yes"
                    s["Visit Date"] = str(visit_date)
                    st.success(f"Visit booked for {selected_school} on {visit_date}.")
                else:
                    st.warning("Please complete the programme before booking a visit.")
else:
    st.info("No schools registered yet.")
