import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Connect to SQLite database
conn = sqlite3.connect("firewise.db", check_same_thread=False)
c = conn.cursor()

# Create schools table if it doesn't exist
c.execute("""
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    status TEXT DEFAULT 'Not Signed Up',
    scheduled_date TEXT,
    completion_date TEXT,
    firefighter_visit_date TEXT
)
""")
conn.commit()

# Helper functions
def add_school(school_name, contact_person, email):
    c.execute("INSERT INTO schools (school_name, contact_person, email) VALUES (?, ?, ?)",
              (school_name, contact_person, email))
    conn.commit()

def get_all_schools():
    return pd.read_sql_query("SELECT * FROM schools", conn)

def update_school_status(school_id, status, scheduled_date=None, completion_date=None, visit_date=None):
    c.execute("""
        UPDATE schools
        SET status = ?, scheduled_date = ?, completion_date = ?, firefighter_visit_date = ?
        WHERE id = ?
    """, (status, scheduled_date, completion_date, visit_date, school_id))
    conn.commit()

# Streamlit UI
st.title("Get Firewise - School Engagement Dashboard")

menu = ["View Schools", "Add School", "Update School"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Schools":
    st.subheader("All Schools and Status")
    df = get_all_schools()
    st.dataframe(df)

elif choice == "Add School":
    st.subheader("Add a New School")
    with st.form(key="add_school_form"):
        school_name = st.text_input("School Name")
        contact_person = st.text_input("Contact Person")
        email = st.text_input("Email")
        submit = st.form_submit_button("Add School")
        if submit:
            if school_name:
                add_school(school_name, contact_person, email)
                st.success(f"Added school: {school_name}")
            else:
                st.error("School name is required.")

elif choice == "Update School":
    st.subheader("Update School Status")
    df = get_all_schools()
    school_names = df["school_name"].tolist()
    selected_school = st.selectbox("Select School", school_names)

    if selected_school:
        school_row = df[df["school_name"] == selected_school].iloc[0]
        school_id = school_row["id"]

        status = st.selectbox("Status", ["Agreed", "Scheduled", "Completed", "Visit Booked"])
        scheduled_date = st.date_input("Scheduled Date", value=date.today()) if status in ["Scheduled", "Completed", "Visit Booked"] else None
        completion_date = st.date_input("Completion Date", value=date.today()) if status in ["Completed", "Visit Booked"] else None
        visit_date = st.date_input("Firefighter Visit Date", value=date.today()) if status == "Visit Booked" else None

        if st.button("Update Status"):
            update_school_status(school_id, status,
                                 scheduled_date.isoformat() if scheduled_date else None,
                                 completion_date.isoformat() if completion_date else None,
                                 visit_date.isoformat() if visit_date else None)
            st.success(f"Updated {selected_school} to status: {status}")
