import streamlit as st

st.title("Tabbed Page View Example")

tabs = st.tabs(["Overview", "Details", "Settings"])

with tabs[0]:
    st.header("Overview")
    st.write("This is the overview tab.")

with tabs[1]:
    st.header("Details")
    st.write("This is the details tab.")

with tabs[2]:
    st.header("Settings")
    st.write("This is the settings tab.")
