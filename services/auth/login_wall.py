import streamlit as st
from services.persistence.cache import get_repo


def render_login_wall() -> bool:
    if st.session_state.get("user_id") is not None:
        return False  # User is already logged in, no need to show the login wall
    
    st.title("🏋️‍♀️ Welcome to AI Gym Coach")
    st.markdown("Please log in to access your personalized workout dashboard.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Start Session")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
            return True  # Show the login wall again
        
        # Get user from database using cached repo
        repo = get_repo()
        user = repo.get_user(username)
        
        if user:
            # In production, verify password hash here
            st.session_state["user_name"] = username
            st.session_state["user_id"] = user["id"]
            st.success(f"Logged in as {username}")
            st.rerun()  # Rerun the app to update the session state and show the main content
        else:
            repo.create_user(username, password)  # In production, hash the password before storing
            st.success("User created. Please log in.")
            return True  # Show the login wall again

    return True  # Show the login wall to the user
