import pandas as pd
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from vision.exercise_video_processor import ExerciseVideoProcessor

def render(data: pd.DataFrame) -> None:
    st.title("🏋️‍♀️ Welcome to AI Gym Coach")
    st.markdown("#### Real-time pose detection and proactive AI voice coaching")

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
 
    st.markdown("#### Workout History")

    # st.dataframe(data)
