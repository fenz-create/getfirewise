import streamlit as st
import pandas as pd

# Dummy data for Pipeline deals
pipeline_data = pd.DataFrame([
    {
        "Owner": "Alice",
        "Contacts": "Greenwood High",
        "Stage": "Qualified",
        "Close Probability": "60%",
        "Estimated Deal": "$12,000"
    },
    {
        "Owner": "Bob",
        "Contacts": "Maple Leaf Academy",
        "Stage": "Proposal",
        "Close Probability": "75%",
        "Estimated Deal": "$18,500"
    },
    {
        "Owner": "Charlie",
        "Contacts": "Riverdale School",
        "Stage": "Negotiation",
        "Close Probability": "85%",
        "Estimated Deal": "$25,000"
    }
])

# Dummy data for Closed Won deals
closed_won_data = pd.DataFrame([
    {
        "Owner": "Diana",
        "Contacts": "Sunrise Elementary",
        "Stage": "Closed Won",
        "Close Probability": "100%",
        "Estimated Deal": "$30,000"
    },
    {
        "Owner": "Ethan",
        "Contacts": "Hilltop School",
        "Stage": "Closed Won",
        "Close Probability": "100%",
        "Estimated Deal": "$22,000"
    }
])

# Function to apply color-coded stage tags
def color_stage(stage):
    color_map = {
        "Qualified": "blue",
        "Proposal": "orange",
        "Negotiation": "purple",
        "Closed Won": "green"
    }
    color = color_map.get(stage, "gray")
    return f"<span style='color:white; background-color:{color}; padding:4px; border-radius:4px'>{stage}</span>"

# Apply color formatting to stage columns
pipeline_data["Stage"] = pipeline_data["Stage"].apply(lambda x: color_stage(x))
closed_won_data["Stage"] = closed_won_data["Stage"].apply(lambda x: color_stage(x))

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Client Relationship Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Pipeline")
    st.write("Deals currently in progress.")
    st.write(pipeline_data.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    st.subheader("✅ Closed Won")
    st.write("Successfully closed deals.")
    st.write(closed_won_data.to_html(escape=False, index=False), unsafe_allow_html=True)
