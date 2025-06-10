import streamlit as st

st.title("School Progress Tracker")

schools = [f"School {i+1}" for i in range(45)]
stages = ["Not Started", "In Progress", "Completed"]
selected_stages = {}

st.sidebar.header("Overall Progress")

completed_count = 0
for school in schools:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.write(school)
    with col2:
        stage = st.selectbox(f"Stage for {school}", stages, key=school)
        selected_stages[school] = stage
        if stage == "Completed":
            completed_count += 1

progress = completed_count / len(schools)
st.sidebar.progress(progress)
st.sidebar.write(f"{completed_count} out of {len(schools)} schools completed ({progress*100:.1f}%)")
