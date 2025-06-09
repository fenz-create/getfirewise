
import streamlit as st
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("firewise.db", check_same_thread=False)
c = conn.cursor()

# Define workflow stages
workflow_stages = [
    "Signed Up",
    "Agreed",
    "Scheduled",
    "Completed",
    "Visit Booked"
]

# Function to get progress percentage
def get_progress(status):
    if status in workflow_stages:
        return (workflow_stages.index(status) + 1) / len(workflow_stages)
    return 0

# Function to update school status and dates
def update_school(school_id, new_status, scheduled_date, completion_date, visit_date):
    c.execute("""
        UPDATE schools
        SET status = ?, scheduled_date = ?, completion_date = ?, firefighter_visit_date = ?
        WHERE id = ?
    """, (new_status, scheduled_date, completion_date, visit_date, school_id))
    conn.commit()

# App title
st.title("Get Firewise - School Engagement Dashboard")

# Load all schools
schools_df = pd.read_sql_query("SELECT * FROM schools", conn)

# Dropdown to select a school
school_names = schools_df["school_name"].tolist()
selected_school_name = st.selectbox("Select a school to update", school_names)

if selected_school_name:
    school = schools_df[schools_df["school_name"] == selected_school_name].iloc[0]
    st.subheader(f"Managing: {school['school_name']}")
    st.markdown(f"**Contact:** {school['contact_person']} ({school['email']})")

    # Show progress bar
    progress = get_progress(school["status"])
    st.progress(progress, text=f"Current Stage: {school['status']}")

    # Determine next stage
    current_index = workflow_stages.index(school["status"]) if school["status"] in workflow_stages else 0
    if current_index < len(workflow_stages) - 1:
        next_stage = workflow_stages[current_index + 1]
        st.markdown(f"### Advance to: {next_stage}")

        # Input fields for relevant dates
        scheduled_date = st.date_input("Scheduled Date", value=pd.to_datetime(school["scheduled_date"]) if school["scheduled_date"] else None)
        completion_date = st.date_input("Completion Date", value=pd.to_datetime(school["completion_date"]) if school["completion_date"] else None)
        visit_date = st.date_input("Firefighter Visit Date", value=pd.to_datetime(school["firefighter_visit_date"]) if school["firefighter_visit_date"] else None)

        if st.button(f"Advance to '{next_stage}'"):
            update_school(
                school_id=school["id"],
                new_status=next_stage,
                scheduled_date=scheduled_date if next_stage in ["Scheduled", "Completed", "Visit Booked"] else school["scheduled_date"],
                completion_date=completion_date if next_stage in ["Completed", "Visit Booked"] else school["completion_date"],
                visit_date=visit_date if next_stage == "Visit Booked" else school["firefighter_visit_date"]
            )
            st.success(f"School advanced to '{next_stage}'")
            st.experimental_rerun()
    else:
        st.info("This school has completed all stages.")

st.markdown("---")
st.subheader("All Schools Overview")
st.dataframe(schools_df)
