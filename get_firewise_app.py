import streamlit as st
import pandas as pd

# Define stages and their corresponding progress values
stages = {
    "Not Started": 0,
    "Signed Up": 25,
    "Agreed": 50,
    "Completing": 75,
    "Completed": 100
}

# Initialize session state for schools
if 'schools' not in st.session_state:
    st.session_state.schools = pd.DataFrame({
        'School Name': [f"School {i+1}" for i in range(45)],
        'Stage': ["Not Started"] * 45
    })

st.title("🔥 Get Firewise Programme - School Progress Tracker")

# Display the table with dropdowns and progress bars
for i in range(len(st.session_state.schools)):
    cols = st.columns([2, 2, 6])
    with cols[0]:
        st.markdown(f"**{st.session_state.schools.at[i, 'School Name']}**")
    with cols[1]:
        selected_stage = st.selectbox(
            label="",
            options=list(stages.keys()),
            index=list(stages.keys()).index(st.session_state.schools.at[i, 'Stage']),
            key=f"stage_{i}"
        )
        st.session_state.schools.at[i, 'Stage'] = selected_stage
    with cols[2]:
        progress = stages[selected_stage] / 100
        st.progress(progress)
