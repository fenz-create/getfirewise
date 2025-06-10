import streamlit as st

# Initialize session state for page tracking
if 'page' not in st.session_state:
    st.session_state.page = 1

# Function to go to the next page
def next_page():
    st.session_state.page += 1

# Function to go to the previous page
def prev_page():
    st.session_state.page -= 1

# Page 1
def page_one():
    st.title("Step 1: Welcome")
    st.write("This is the first step of the process.")
    if st.button("Next"):
        next_page()

# Page 2
def page_two():
    st.title("Step 2: Information")
    st.write("Please review the information on this page.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            prev_page()
    with col2:
        if st.button("Next"):
            next_page()

# Page 3
def page_three():
    st.title("Step 3: Confirmation")
    st.write("You have reached the final step.")
    if st.button("Back"):
        prev_page()
    st.success("Process complete!")

# Page routing
if st.session_state.page == 1:
    page_one()
elif st.session_state.page == 2:
    page_two()
elif st.session_state.page == 3:
    page_three()
