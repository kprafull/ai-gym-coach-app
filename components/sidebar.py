import streamlit as st


def render() -> None:
    st.sidebar.title("AI Gym App")
    st.sidebar.markdown("Customize the app settings and view options.")
    st.sidebar.selectbox("Choose view", ["Overview", "Data"])  # placeholder
