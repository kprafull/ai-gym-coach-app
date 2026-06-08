import pandas as pd
import streamlit as st
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from vision.exercise_video_processor import ExerciseVideoProcessor
from services.tracking.metrics import sync_metrics_to_session
from services.persistence.cache import get_repo
from services.coaching.voice_pipeline import autoplay_audio

def render() -> None:
    st.title("🏋️‍♀️ Welcome to AI Gym Coach")
    st.markdown("#### Real-time pose detection and proactive AI voice coaching")

    if st.session_state.get("audio_to_play"):
        autoplay_audio(st.session_state.audio_to_play)

    if st.session_state.get("coach_feedback"):
        st.markdown("")
        st.success(f"🤖 **Coach:** {st.session_state.coach_feedback}")

    workout_started = st.session_state.get("workout_started", False)

    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 7px dashed #444;
                border-radius: 0px;
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,<br>
                    then click <strong>Start Workout</strong> to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=ExerciseVideoProcessor,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            async_processing=True
        )   
        
        sync_metrics_to_session(context)

        if context and context.state.playing:
            st.markdown("#### Exercise Analysis")
            st.info("Camera is active. Perform your exercise in view of the camera for real-time feedback and metrics.")
            # time.sleep(0.25)
            # st.rerun()  # Trigger a rerun to update the UI with the latest metrics

    st.divider()
    st.markdown("#### Workout History")
    user_id = st.session_state.get("user_id")
    if user_id:
        history = get_repo().get_user_exercises(user_id)
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df)
        else:
            st.info("No workout history found. Start your first workout to see it here!")