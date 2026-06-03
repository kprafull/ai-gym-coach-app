import streamlit as st

def render_login_wall() -> bool:
    if st.session_state.get("user_id") is not None:
        return False # User is already logged in, no need to show the login wall
    
    st.title("🏋️‍♀️ Welcome to AI Gym Coach")
    st.markdown("Please log in to access your personalized workout dashboard.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Start Session")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
            return True # Show the login wall again
        # Here you would normally validate the username and password
        # For this example, we'll just simulate a successful login
        st.session_state["user_name"] = username  # Simulate setting a user ID in session state
        st.session_state["user_id"] = 1  # Simulate with user id 1
        st.success(f"Logged in as {username}")
        st.rerun()  # Rerun the app to update the session state and show the main content

    return True # Show the login wall to the user
