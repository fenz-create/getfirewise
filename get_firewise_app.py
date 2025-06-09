import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

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
    status TEXT DEFAULT 'Signed Up',
    scheduled_date TEXT,
    completion_date TEXT,
    firefighter_visit_date TEXT
)
""")
conn.commit()

# Workflow stages
workflow_stages = ["Signed Up", "Agreed", "Scheduled", "Completed", "Visit Booked"]

# Helper to get progress index
def get_progress_index(status):
    return workflow_stages.index(status) + 1 if status in workflow_stages else 1

# Add new school
def add_school(school_name, contact_person, email):
    c.execute("INSERT INTO schools (school_name, contact_person, email) VALUES (?, ?, ?)",
              (school_name, contact_person, email))
    conn.commit()

# Update school status and dates
def update_school_status(school_id, status, date_field=None, date_value=None):
    if date_field and date_value:
        c.execute(f"UPDATE schools SET status = ?, {date_field} = ? WHERE id = ?", (status, date_value, school_id))
    else:
        c.execute("UPDATE schools SET status = ? WHERE id = ?", (status, school_id))
    conn.commit()

# Load all schools
def load_schools():
    return pd.read_sql_query("SELECT * FROM schools", conn)

# UI
st.set_page_config(page_title="Get Firewise Tracker", layout="wide")
st.title("🔥 Get Firewise Programme Tracker")

# Add new school
with st.expander("➕ Add New School"):
    with st.form("add_school_form"):
        school_name = st.text_input("School Name")
        contact_person = st.text_input("Contact Person")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add School")
        if submitted and school_name:
            add_school(school_name, contact_person, email)
            st.success(f"{school_name} added successfully!")

# Load and display schools
df = load_schools()
if df.empty:
    st.info("No schools have signed up yet.")
else:
    for idx, row in df.iterrows():
        st.markdown("---")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader(row["school_name"])
            st.write(f"📧 {row['email']} | 👤 {row['contact_person']}")
            st.progress(get_progress_index(row["status"]) / len(workflow_stages))
            st.write(f"**Current Stage:** {row['status']}")
        with col2:
            if row["status"] == "Signed Up":
                if st.button("✅ Mark Agreed", key=f"agree_{row['id']}"):
                    update_school_status(row["id"], "Agreed")
                    st.experimental_rerun()
            elif row["status"] == "Agreed":
                scheduled_date = st.date_input("📅 Schedule Programme", key=f"schedule_{row['id']}")
                if st.button("📌 Confirm Schedule", key=f"confirm_schedule_{row['id']}"):
                    update_school_status(row["id"], "Scheduled", "scheduled_date", scheduled_date.isoformat())
                    st.experimental_rerun()
            elif row["status"] == "Scheduled":
                completion_date = st.date_input("✅ Confirm Completion", key=f"complete_{row['id']}")
                if st.button("✔️ Mark Completed", key=f"mark_complete_{row['id']}"):
                    update_school_status(row["id"], "Completed", "completion_date", completion_date.isoformat())
                    st.experimental_rerun()
            elif row["status"] == "Completed":
                visit_date = st.date_input("🚒 Book Firefighter Visit", key=f"visit_{row['id']}")
                if st.button("📅 Book Visit", key=f"book_visit_{row['id']}"):
                    update_school_status(row["id"], "Visit Booked", "firefighter_visit_date", visit_date.isoformat())
                    st.experimental_rerun()
            elif row["status"] == "Visit Booked":
                st.success("🎉 Workflow complete!")
