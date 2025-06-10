import streamlit as st
import pandas as pd
import uuid
import time

# Set page layout
st.set_page_config(layout="wide")
st.title("School Engagement Dashboard")

# Initialize session state
if 'school_data' not in st.session_state:
    st.session_state.school_data = pd.DataFrame([
        {
            "School Name": "Greenwood High",
            "Firewise Teacher": "Alice Johnson",
            "Email": "alice@greenwood.edu",
            "Phone": "123-456-7890",
            "Website": "https://greenwood.edu",
            "Stage": "Agreed"
        },
        {
            "School Name": "Maple Leaf Academy",
            "Firewise Teacher": "Brian Smith",
            "Email": "brian@mapleleaf.edu",
            "Phone": "234-567-8901",
            "Website": "https://mapleleaf.edu",
            "Stage": "Agreed"
        },
        {
            "School Name": "Riverdale School",
            "Firewise Teacher": "Catherine Lee",
            "Email": "catherine@riverdale.edu",
            "Phone": "345-678-9012",
            "Website": "https://riverdale.edu",
            "Stage": "Completing"
        },
        {
            "School Name": "Sunrise Elementary",
            "Firewise Teacher": "David Kim",
            "Email": "david@sunrise.edu",
            "Phone": "456-789-0123",
            "Website": "https://sunrise.edu",
            "Stage": "Completing"
        },
        {
            "School Name": "Hilltop School",
            "Firewise Teacher": "Emma Brown",
            "Email": "emma@hilltop.edu",
            "Phone": "567-890-1234",
            "Website": "https://hilltop.edu",
            "Stage": "Firefighter Visit"
        },
        {
            "School Name": "Lakeside Academy",
            "Firewise Teacher": "Frank Green",
            "Email": "frank@lakeside.edu",
            "Phone": "678-901-2345",
            "Website": "https://lakeside.edu",
            "Stage": "Firefighter Visit"
        }
    ])

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

if 'show_form' not in st.session_state:
    st.session_state.show_form = False

if 'last_notification' not in st.session_state:
    st.session_state.last_notification = time.time()

# 🔔 In-app toast notification every 30 seconds
if time.time() - st.session_state.last_notification > 30:
    st.toast("📣 Paihia School is finishing Get Firewise!")
    st.session_state.last_notification = time.time()
    st.rerun()

# Top-right toggle button
top_cols = st.columns([10, 1])
with top_cols[1]:
    if st.session_state.show_form:
        if st.button("➖", key="toggle_form"):
            st.session_state.show_form = False
            st.session_state.edit_index = None
    else:
        if st.button("➕", key="toggle_form"):
            st.session_state.show_form = True
            st.session_state.edit_index = None

# Add or edit school form
def add_or_edit_school_form():
    if not st.session_state.show_form and st.session_state.edit_index is None:
        return

    is_editing = st.session_state.edit_index is not None
    st.subheader("Edit School" if is_editing else "Add New School")

    if is_editing:
        school = st.session_state.school_data.loc[st.session_state.edit_index]
    else:
        school = {}

    with st.form("school_form"):
        name = st.text_input("School Name", value=school.get("School Name", ""))
        teacher = st.text_input("Firewise Teacher Name", value=school.get("Firewise Teacher", ""))
        email = st.text_input("Email", value=school.get("Email", ""))
        phone = st.text_input("Phone Number", value=school.get("Phone", ""))
        website = st.text_input("Website", value=school.get("Website", ""))
        stage = st.selectbox("Stage", ["Agreed", "Completing", "Firefighter Visit"],
                             index=["Agreed", "Completing", "Firefighter Visit"].index(school.get("Stage", "Agreed")))

        submitted = st.form_submit_button("Update" if is_editing else "Add")
        cancel = st.form_submit_button("Cancel")

        if submitted:
            new_entry = {
                "School Name": name,
                "Firewise Teacher": teacher,
                "Email": email,
                "Phone": phone,
                "Website": website,
                "Stage": stage
            }
            if is_editing:
                st.session_state.school_data.loc[st.session_state.edit_index] = new_entry
                st.success("School updated successfully!")
            else:
                st.session_state.school_data = pd.concat([
                    st.session_state.school_data,
                    pd.DataFrame([new_entry])
                ], ignore_index=True)
                st.success("School added successfully!")
            st.session_state.edit_index = None
            st.session_state.show_form = False
            st.experimental_rerun()

        if cancel:
            st.session_state.edit_index = None
            st.session_state.show_form = False
            st.experimental_rerun()

# Display table with edit buttons
def display_table(df, stage_name):
    st.subheader(f"{stage_name} Schools")
    search = st.text_input(f"Search {stage_name}", key=f"search_{stage_name}")
    filtered_df = df.copy()
    if search:
        filtered_df = df[df.apply(
            lambda row: search.lower() in row["School Name"].lower() or search.lower() in row["Firewise Teacher"].lower(),
            axis=1
        )]

    for i in filtered_df.index:
        row = filtered_df.loc[i]
        cols = st.columns([3, 3, 3, 3, 3, 2, 1])
        cols[0].markdown(f"**{row['School Name']}**")
        cols[1].write(row["Firewise Teacher"])
        cols[2].write(row["Email"])
        cols[3].markdown(f"[{row['Phone']}](tel:{row['Phone']})")  # tel: link
        cols[4].markdown(f"Visit Site")
        cols[5].write(row["Stage"])
        if cols[6].button("✏️", key=f"edit_{uuid.uuid4()}"):
            st.session_state.edit_index = i
            st.session_state.show_form = True
            st.experimental_rerun()

# Tabs
tab_names = ["Overview", "Agreed", "Completing", "Firefighter Visit"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        if tab_names[i] == "Overview":
            add_or_edit_school_form()
            display_table(st.session_state.school_data, "Overview")
        else:
            stage_df = st.session_state.school_data[st.session_state.school_data["Stage"] == tab_names[i]]
            display_table(stage_df, tab_names[i])
