
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Dummy data for Pipeline deals
pipeline_data = pd.DataFrame([
    {"Owner": "Alice", "Contacts": "Greenwood High", "Stage": "Qualified", "Close Probability": "60%", "Estimated Deal": "$12,000"},
    {"Owner": "Bob", "Contacts": "Maple Leaf Academy", "Stage": "Proposal", "Close Probability": "75%", "Estimated Deal": "$18,500"},
    {"Owner": "Charlie", "Contacts": "Riverdale School", "Stage": "Negotiation", "Close Probability": "85%", "Estimated Deal": "$25,000"}
])

# Dummy data for Closed Won deals
closed_won_data = pd.DataFrame([
    {"Owner": "Diana", "Contacts": "Sunrise Elementary", "Stage": "Closed Won", "Close Probability": "100%", "Estimated Deal": "$30,000"},
    {"Owner": "Ethan", "Contacts": "Hilltop School", "Stage": "Closed Won", "Close Probability": "100%", "Estimated Deal": "$22,000"}
])

st.set_page_config(layout="wide")
st.title("Client Relationship Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Pipeline")
    gb1 = GridOptionsBuilder.from_dataframe(pipeline_data)
    gb1.configure_default_column(editable=True)
    grid_response1 = AgGrid(pipeline_data, gridOptions=gb1.build(), update_mode=GridUpdateMode.VALUE_CHANGED)
    updated_pipeline_data = grid_response1['data']

with col2:
    st.subheader("✅ Closed Won")
    gb2 = GridOptionsBuilder.from_dataframe(closed_won_data)
    gb2.configure_default_column(editable=True)
    grid_response2 = AgGrid(closed_won_data, gridOptions=gb2.build(), update_mode=GridUpdateMode.VALUE_CHANGED)
    updated_closed_won_data = grid_response2['data']
