
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# Database setup
conn = sqlite3.connect("firewise.db", check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT,
    email TEXT,
    status TEXT,
    scheduled_date TEXT,
    completion_date TEXT,
    visit_date TEXT
)
""")
conn.commit()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# User authentication
def register_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    data = c.fetchone()
    if data and verify_password(password, data[0]):
        return True
    return False

# School management
def add_school(name, contact, email):
    c.execute("INSERT INTO schools (name, contact, email, status) VALUES (?, ?, ?, ?)", (name, contact, email, "Not Signed Up"))
    conn.commit()

def get_schools():
    c.execute("SELECT * FROM schools")
    return c.fetchall()

def update_school_status(school_id, status, date_field=None, date_value=None):
    if date_field and date_value:
        c.execute(f"UPDATE schools SET status = ?, {date_field} = ? WHERE id = ?", (status, date_value, school_id))
    else:
        c.execute("UPDATE schools SET status = ? WHERE id = ?", (status, school_id))
    conn.commit()

# Streamlit UI
st.set_page_config(page_title="Get Firewise App", layout="wide")
st.title("🔥 Get Firewise School Engagement App")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login/Register
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            try:
                register_user(new_user, new_pass)
                st.success("User registered! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
else:
    # Main app
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["School Tracker", "Staff Dashboard", "Add School"])

    if page == "School Tracker":
        st.subheader("📋 School Tracker")
        schools = get_schools()
        st.dataframe(schools, use_container_width=True)

    elif page == "Staff Dashboard":
        st.subheader("🧑‍🚒 Staff Dashboard")
        schools = get_schools()
        for school in schools:
            with st.expander(f"{school[1]} ({school[4]})"):
                st.write(f"Contact: {school[2]} | Email: {school[3]}")
                new_status = st.selectbox("Update Status", ["Agreed", "Scheduled", "Completed", "Visit Booked"], key=f"status_{school[0]}")
                date_input = None
                if new_status == "Scheduled":
                    date_input = st.date_input("Scheduled Date", key=f"scheduled_{school[0]}")
                    if st.button("Update", key=f"update_{school[0]}"):
                        update_school_status(school[0], new_status, "scheduled_date", date_input.strftime("%Y-%m-%d"))
                        st.success("Status updated.")
                elif new_status == "Completed":
                    date_input = st.date_input("Completion Date", key=f"completed_{school[0]}")
                    if st.button("Update", key=f"update_{school[0]}"):
                        update_school_status(school[0], new_status, "completion_date", date_input.strftime("%Y-%m-%d"))
                        st.success("Status updated.")
                elif new_status == "Visit Booked":
                    date_input = st.date_input("Firefighter Visit Date", key=f"visit_{school[0]}")
                    if st.button("Update", key=f"update_{school[0]}"):
                        update_school_status(school[0], new_status, "visit_date", date_input.strftime("%Y-%m-%d"))
                        st.success("Status updated.")
                else:
                    if st.button("Update", key=f"update_{school[0]}"):
                        update_school_status(school[0], new_status)
                        st.success("Status updated.")

    elif page == "Add School":
        st.subheader("➕ Add New School")
        name = st.text_input("School Name")
        contact = st.text_input("Contact Person")
        email = st.text_input("Email")
        if st.button("Add School"):
            if name and contact and email:
                add_school(name, contact, email)
                st.success("School added successfully!")
            else:
                st.error("Please fill in all fields.")
