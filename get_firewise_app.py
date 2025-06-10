import streamlit as st
import pandas as pd

# Set page layout
st.set_page_config(layout="wide")
st.title("School Engagement Dashboard")

# Define unique dummy data for each stage
agreed_schools = pd.DataFrame([
    {"School Name": "Greenwood High", "Contact": "Alice Johnson (alice@greenwood.edu)", "Website": '<a href="https://greenwood.edu" target="_blank">Visit Site</a>', "Stage": "Agreed"},
    {"School Name": "Maple Leaf Academy", "Contact": "Brian Smith (brian@mapleleaf.edu)", "Website": '<a href="https://mapleleaf.edu" target="_blank">Visit Site</a>', "Stage": "Agreed"}
])

completing_schools = pd.DataFrame([
    {"School Name": "Riverdale School", "Contact": "Catherine Lee (catherine@riverdale.edu)", "Website": '<a href="https://riverdale.edu" target="_blank">Visit Site</a>', "Stage": "Completing"},
    {"School Name": "Sunrise Elementary", "Contact": "David Kim (david@sunrise.edu)", "Website": '<a href="https://sunrise.edu" target="_blank">Visit Site</a>', "Stage": "Completing"}
])

firefighter_schools = pd.DataFrame([
    {"School Name": "Hilltop School", "Contact": "Emma Brown (emma@hilltop.edu)", "Website": '<a href="https://hilltop.edu" target="_blank">Visit Site</a>', "Stage": "Firefighter Visit"},
    {"School Name": "Lakeside Academy", "Contact": "Frank Green (frank@lakeside.edu)", "Website": '<a href="https://lakeside.edu" target="_blank">Visit Site</a>', "Stage": "Firefighter Visit"}
])

# Combine all for overview
overview_schools = pd.concat([agreed_schools, completing_schools, firefighter_schools], ignore_index=True)

# Tab names
tab_names = ["Overview", "Agreed", "Completing", "Firefighter Visit"]
tabs = st.tabs(tab_names)

# Display searchable tables in each tab
for i, tab in enumerate(tabs):
    with tab:
        if tab_names[i] == "Overview":
            df = overview_schools.copy()
        elif tab_names[i] == "Agreed":
            df = agreed_schools.copy()
        elif tab_names[i] == "Comple
