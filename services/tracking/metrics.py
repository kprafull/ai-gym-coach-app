import time

import streamlit as st
from services.config.workout_config import METRICS_FIELDS
from services.persistence.cache import get_repo

def sync_metrics_to_session(context):
    """
    Syncs the latest exercise metrics to Streamlit's session state for real-time display.
    """
    if not context or not hasattr(context, "state") or not context.state.playing:
        return

    processor = getattr(context, "video_processor", None)  # Ensure video_processor exists

    if not processor:
        return

    exercise = st.session_state.get("plan_exercise")

    if not exercise:
        return
    
    processor.set_exercise_type(exercise)

    latest_metrics = processor.get_latest_metrics()

    if not latest_metrics:
        return
    
    reps = latest_metrics.get("reps", 0)
    st.session_state.reps = reps

    reps_per_set = st.session_state.get("plan_reps", 1)
    sets_completed = reps // reps_per_set if reps_per_set else 0
    current_set_reps = reps % reps_per_set if reps_per_set else reps
    st.session_state.current_set_reps = current_set_reps
    st.session_state.sets_completed = sets_completed
    plan_sets = st.session_state.get("plan_sets", 0)
    workout_completed = sets_completed >= plan_sets
    st.session_state.workout_completed = workout_completed
    # print(f"Syncing metrics to session: {latest_metrics}")

    fields = METRICS_FIELDS.get(exercise)

    if fields is None:
        print(f"No metric fields defined for exercise '{exercise}'. Skipping session sync.")
        return
    
    for key, default in fields.items():
        st.session_state[key] = latest_metrics.get(key, default)


    last_saved_sets = st.session_state.get("last_saved_set_completed", 0)
    if plan_sets > 0 and reps_per_set > 0 and sets_completed > last_saved_sets:
        newly_completed_sets = sets_completed - last_saved_sets
        now_ts = time.time()
        started_at = st.session_state.get("set_cycle_start_time", now_ts)
        time_taken = now_ts - started_at
        user_id = st.session_state.get("user_id")
        get_repo().add_exercise(user_id, exercise, reps_per_set * newly_completed_sets, newly_completed_sets, int(time_taken))

        if st.session_state.get("voice_pipeline"):
            result = st.session_state.voice_pipeline.process_event(
                event="set_completed",
                exercise=exercise,
                metrics=latest_metrics,
            )

            if result:
                st.session_state.audio_to_play, st.session_state.coach_feedback = result

        st.session_state["last_saved_set_completed"] = sets_completed
        st.session_state["set_cycle_start_time"] = now_ts  # Reset start time for



    if workout_completed and st.session_state.get("workout_started"):
        st.session_state.workout_started = False

        if st.session_state.get("voice_pipeline"):
            result = st.session_state.voice_pipeline.process_event(
                event="workout_completed",
                exercise=exercise,
                metrics=latest_metrics,
            )

            if result:
                st.session_state.audio_to_play, st.session_state.coach_feedback = result
                
    pose_detected = latest_metrics.get("pose_detected", True)
    
    if not pose_detected and st.session_state.get("voice_pipeline") and not workout_completed:
        result = st.session_state.voice_pipeline.process_event(
            event="no_pose_detected",
            exercise=exercise,
            metrics={"issue": "No pose detected! Please step into the camera frame."},
        )
    
        if result:
            st.session_state.audio_to_play, st.session_state.coach_feedback = result

    if st.session_state.get("voice_pipeline") and not workout_completed:
        result = st.session_state.voice_pipeline.process_event(
            event="ongoing_form_check",
            exercise=exercise,
            metrics=latest_metrics,
        )
        
        if result:
            st.session_state.audio_to_play, st.session_state.coach_feedback = result
