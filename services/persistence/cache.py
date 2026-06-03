"""Streamlit cache for database resources."""

import streamlit as st
from services.persistence.exercise_repository import ExerciseRepository

@st.cache_resource
def get_repo() -> ExerciseRepository:
    """Cached singleton instance of ExerciseRepository for the Streamlit app."""
    return ExerciseRepository()
