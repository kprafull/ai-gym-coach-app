import pandas as pd
import streamlit as st


def render(data: pd.DataFrame) -> None:
    st.title("🏋️‍♀️ Welcome to AI Gym Coach")
    st.header("Workout Summary")
    st.dataframe(data)
    st.markdown("Use this area to build charts and analytics for training progress.")
