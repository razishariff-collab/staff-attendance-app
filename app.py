import streamlit as st
from datetime import datetime

# Initialize session state variables
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "attendance" not in st.session_state:
    team_members = [
        "Razi", "Pradeep", "Jagan", "Logash", 
        "Madushan", "Aluwihare", "Buddika"
    ]
    st.session_state.attendance = {
        name: {"status": "Out", "history": []} for name in team_members
    }

# --- SCREEN 1: LOGIN ---
if st.session_state.logged_in_user is None:
    st.title("🔐 Staff Attendance Login")
    st.write("Enter your name to log in.")

    with st.form("login_form"):
        name_input = st.text_input("Your Name")
        submit = st.form_submit_button("Login")

        if submit:
            clean_name = name_input.strip().capitalize()
            if not clean_name:
                st.error("Please enter a name.")
            else:
                st.session_state.logged_in_user = clean_name
                if clean_name not in st.session_state.attendance:
                    st.session_state.attendance[clean_name] = {"status": "Out", "history": []}
                st.rerun()
else:
    # --- SCREEN 2: DASHBOARD & REPORTS ---
    user = st.session_state.logged_in_user
    st.title(f"Welcome, {user}!")
    
    user_data = st.session_state.attendance[user]
    current_status = user_data["status"]
    st.write(f"Current Status: **{current_status}**")

    col1, col2 = st.columns(2)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with col1:
        if st.button("Clock In"):
            if current_status == "In":
                st.warning("You are already clocked in!")
            else:
                user_data["status"] = "In"
                user_data["history"].append(f"Clocked In at {current_time}")
                st.success("Successfully clocked in!")
                st.rerun()

    with col2:
        if st.button("Clock Out"):
            if current_status == "Out":
                st.warning("You are already clocked out!")
            else:
                user_data["status"] = "Out"
                user_data["history"].append(f"Clocked Out at {current_time}")
                st.success("Successfully clocked out!")
                st.rerun()

    # Display Personal History
    st.divider()
    st.subheader("⏱️ Your Attendance History")
    if user_data["history"]:
        for record in reversed(user_data["history"]):
            st.write(f"- {record}")
    else:
        st.info("No check-in history yet.")

    # Display Full Team Report
    st.divider()
    st.subheader("📊 Team Attendance Report")
    st.write("Overview of all staff members:")

    for staff_name, data in st.session_state.attendance.items():
        with st.expander(f"{staff_name} — Status: {data['status']}"):
            if data["history"]:
                for h in reversed(data["history"]):
                    st.text(f"• {h}")
            else:
                st.text("No activity recorded yet.")

    st.divider()
    if st.button("Log Out"):
        st.session_state.logged_in_user = None
        st.rerun()