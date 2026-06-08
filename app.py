import streamlit as st
import os

from components import main as main_component
from components import sidebar as sidebar_component
from data import load_data
from services.auth.login_wall import render_login_wall
from services.states.session_defaults import initial_session_defaults
from groq import Groq

from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio


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

    if "voice_pipeline" not in st.session_state:

        try:
            api_key = os.environ.get("GROQ_API_KEY", "")

            if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            
            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)
        except Exception as e:
            st.session_state.voice_pipeline = None
            print("error creating voice pipeline", e)

    sidebar_component.render()
    main_component.render()

if __name__ == "__main__":
    main()
