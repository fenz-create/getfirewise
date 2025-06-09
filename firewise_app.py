import streamlit as st
import sqlite3
import hashlib

DB_NAME = 'firewise.db'

def create_connection():
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result

def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_schools():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schools")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_school(name, contact, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schools (school_name, contact_person, email, status) VALUES (?, ?, ?, ?)",
                   (name, contact, email, 'Not Signed Up'))
    conn.commit()
    conn.close()

def update_school_status(school_id, status, scheduled=None, completed=None, visit=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schools SET status=?, scheduled_date=?, completion_date=?, firefighter_visit_date=? WHERE id=?",
        (status, scheduled, completed, visit, school_id)
    )
    conn.commit()
    conn.close()

def main():
    st.title("Get Firewise School Engagement App")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Staff Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if verify_user(username, password):
                st.success(f"Welcome {username}")
                app_dashboard()
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created successfully")
            else:
                st.error("Username already exists")

def app_dashboard():
    st.subheader("School Tracker and Staff Dashboard")

    menu = ["View Schools", "Add School", "Update School"]
    choice = st.selectbox("Options", menu)

    if choice == "View Schools":
        schools = get_schools()
        for s in schools:
            st.write(f"**{s[1]}** - Status: {s[4]}")
            st.write(f"Contact: {s[2]}, Email: {s[3]}")
            st.write(f"Scheduled: {s[5]}, Completed: {s[6]}, Visit: {s[7]}")
            st.markdown("---")

    elif choice == "Add School":
        name = st.text_input("School Name")
        contact = st.text_input("Contact Person")
        email = st.text_input("Email")
        if st.button("Add"):
            add_school(name, contact, email)
            st.success("School added successfully")

    elif choice == "Update School":
        schools = get_schools()
        school_dict = {f"{s[0]} - {s[1]}": s[0] for s in schools}
        selected = st.selectbox("Select School", list(school_dict.keys()))
        school_id = school_dict[selected]
        status = st.selectbox("Update Status", ["Agreed", "Scheduled", "Completed", "Visit Booked"])
        scheduled = st.date_input("Scheduled Date")
        completed = st.date_input("Completion Date")
        visit = st.date_input("Firefighter Visit Date")
        if st.button("Update"):
            update_school_status(school_id, status, str(scheduled), str(completed), str(visit))
            st.success("School status updated")

if __name__ == '__main__':
    main()
