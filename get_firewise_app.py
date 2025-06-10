import streamlit as st
import datetime

# Initialize session state for school data
if 'school_data' not in st.session_state:
    st.session_state.school_data = {
        'name': '',
        'status': 'Not Signed Up',
        'completion_date': None,
        'visit_booked': False
    }

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", [
    "Sign Up", 
    "Agreement & Completion Date", 
    "Completing Programme", 
    "Book Firefighter Visit"
])

# Page 1: Sign Up
if page == "Sign Up":
    st.title("Get Firewise - School Sign Up")
    school_name = st.text_input("Enter School Name")
    if st.button("Sign Up"):
        if school_name:
            st.session_state.school_data['name'] = school_name
            st.session_state.school_data['status'] = 'Signed Up'
            st.success(f"{school_name} has signed up for the Get Firewise programme.")
        else:
            st.error("Please enter a school name.")

# Page 2: Agreement & Completion Date
elif page == "Agreement & Completion Date":
    st.title("Agreement Confirmation and Completion Date")
    if st.session_state.school_data['status'] == 'Signed Up':
        agreed = st.checkbox("School agrees to the programme")
        completion_date = st.date_input("Set expected completion date", min_value=datetime.date.today())
        if st.button("Confirm Agreement"):
            if agreed:
                st.session_state.school_data['status'] = 'Agreed'
                st.session_state.school_data['completion_date'] = completion_date
                st.success("Agreement confirmed and completion date set.")
            else:
                st.error("Please confirm agreement to proceed.")
    else:
        st.warning("School must sign up first.")

# Page 3: Completing Programme
elif page == "Completing Programme":
    st.title("Update Status to Completing Programme")
    if st.session_state.school_data['status'] == 'Agreed':
        if st.button("Move to Completing Programme"):
            st.session_state.school_data['status'] = 'Completing Programme'
            st.success("School status updated to Completing Programme.")
    else:
        st.warning("School must agree to the programme first.")

# Page 4: Book Firefighter Visit
elif page == "Book Firefighter Visit":
    st.title("Book a Firefighter Visit")
    today = datetime.date.today()
    if st.session_state.school_data['status'] == 'Completing Programme':
        if st.session_state.school_data['completion_date'] and today >= st.session_state.school_data['completion_date']:
            if not st.session_state.school_data['visit_booked']:
                if st.button("Book Firefighter Visit"):
                    st.session_state.school_data['visit_booked'] = True
                    st.success("Firefighter visit booked successfully.")
            else:
                st.info("Firefighter visit already booked.")
        else:
            st.warning("Completion date not reached yet.")
    else:
        st.warning("School must be in Completing Programme status to book a visit.")
