import streamlit as st

from components import main as main_component
from components import sidebar as sidebar_component
from data import load_data
from services.auth.login_wall import render_login_wall
from services.states.session_defaults import initial_session_defaults

def main() -> None:
    st.set_page_config(
        page_title="🏋️‍♀️ AI Gym Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    # Check if the user is logged in
    if render_login_wall():
        return  # Stop further execution if the login wall is shown

    initial_session_defaults()

    sidebar_component.render()

    data = load_data.get_sample_data()
    main_component.render(data)

if __name__ == "__main__":
    main()
