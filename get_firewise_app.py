import streamlit as st
import pandas as pd

# Dummy school data
def generate_school_data():
    return pd.DataFrame([
        {
            "School Name": "Greenwood High",
            "Contact": "Alice Johnson (alice@greenwood.edu)",
            "Website": '<a href="https://greenwood.edu" target="_blank">Visit Site</a>'
        },
        {
            "School Name": "Maple Leaf Academy",
            "Contact": "Brian Smith (brian@mapleleaf.edu)",
            "Website": '<a href="https://mapleleaf.edu" target="_blank">Visit Site</a>'
        },
        {
            "School Name": "Riverdale School",
            "Contact": "Catherine Lee (catherine@riverdale.edu)",
            "Website": '<a href="https://riverdale.edu" target="_blank">Visit Site</a>'
        },
        {
            "School Name": "Sunrise Elementary",
            "Contact": "David Kim (david@sunrise.edu)",
            "Website": '<a href="https://sunrise.edu" target="_blank">Visit Site</a>'
        },
        {
            "School Name": "Hilltop School",
            "Contact": "Emma Brown (emma@hilltop.edu)",
            "Website": '<a href="https://hilltop.edu" target="_blank">Visit Site</a>'
        }
    ])

# Set page layout
st.set_page_config(layout="wide")
st.title("School Engagement Dashboard")

# Tab names
tab_names = ["Overview", "Agreed", "Completing", "Firefighter Visit"]
tabs = st.tabs(tab_names)

# Display searchable tables in each tab
for i, tab in enumerate(tabs):
    with tab:
        st.subheader(f"{tab_names[i]} Schools")
        df = generate_school_data()
        search = st.text_input("Search by school name or contact", key=f"search_{i}")
        if search:
            df = df[df.apply(lambda row: search.lower() in row["School Name"].lower() or search.lower() in row["Contact"].lower(), axis=1)]
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
