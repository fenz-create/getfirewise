import streamlit as st
import sqlite3
import hashlib

# Database connection
conn = sqlite3.connect("firewise.db", check_same_thread=False)
c = conn.cursor()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication
def register_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    return c.fetchone()

# School data functions
def add_school(name, contact, email):
    c.execute("INSERT INTO schools (school_name, contact_person, email) VALUES (?, ?, ?)", (name, contact, email))
    conn.commit()

def get_schools():
    c.execute("SELECT * FROM schools")
    return c.fetchall()

def update_school_status(school_id, status, scheduled=None, completed=None, visit=None):
    c.execute("UPDATE schools SET status = ?, scheduled_date = ?, completion_date = ?, firefighter_visit_date = ? WHERE id = ?",
              (status, scheduled, completed, visit, school_id))
    conn.commit()

# App layout
def main():
    st.title("Get Firewise - School Engagement App")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Register"):
            register_user(new_user, new_password)
            st.success("Account created successfully")

    elif choice == "Login":
        st.subheader("Login to Dashboard")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.success(f"Welcome {username}")
                dashboard()
            else:
                st.error("Invalid credentials")

def dashboard():
    st.subheader("Staff Dashboard")

    menu = ["View Schools", "Add School", "Update School Status"]
    choice = st.selectbox("Options", menu)

    if choice == "View Schools":
        schools = get_schools()
        for s in schools:
            st.write(f"ID: {s[0]}, Name: {s[1]}, Status: {s[4]}, Scheduled: {s[5]}, Completed: {s[6]}, Visit: {s[7]}")

    elif choice == "Add School":
        name = st.text_input("School Name")
        contact = st.text_input("Contact Person")
        email = st.text_input("Email")
        if st.button("Add School"):
            add_school(name, contact, email)
            st.success("School added successfully")

    elif choice == "Update School Status":
        school_id = st.number_input("School ID", min_value=1, step=1)
        status = st.selectbox("Status", ["Agreed", "Scheduled", "Completed", "Visit Booked"])
        scheduled = st.date_input("Scheduled Date")
        completed = st.date_input("Completion Date")
        visit = st.date_input("Firefighter Visit Date")
        if st.button("Update Status"):
            update_school_status(school_id, status, str(scheduled), str(completed), str(visit))
            st.success("School status updated")

if __name__ == '__main__':
    main()
