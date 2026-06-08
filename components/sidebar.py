import time

import streamlit as st
from services.config.workout_config import EXERCISE_OPTIONS

def render() -> None:
    with st.sidebar:
        st.title("🏋️ AI Coach")
        st.caption(f"👤 Logged in as {st.session_state['user_name']}")

        workout_started = st.session_state.get("workout_started", False)

        if not workout_started:
            st.markdown("### Workout Plan")
            plan_exercise = st.selectbox("Choose exercise", EXERCISE_OPTIONS)
            selected_plan_sets = st.number_input(
                "Target sets",
                min_value=1,
                max_value=10,
                value=st.session_state.get("plan_sets", 3),
                step=1,
                key="selected_plan_sets",
            )
            selected_plan_reps = st.number_input(
                "Reps per set",
                min_value=1,
                max_value=50,
                value=st.session_state.get("plan_reps", 10),
                step=1,
                key="selected_plan_reps",
            )
            start_workout_button = st.button("Start Workout", key="start_workout", width="stretch")
            if start_workout_button:
                st.session_state["plan_exercise"] = plan_exercise
                st.session_state["current_set_reps"] = 0
                st.session_state["sets_completed"] = 0
                st.session_state["reps"] = 0
                st.session_state["plan_sets"]=selected_plan_sets
                st.session_state["plan_reps"]=selected_plan_reps
                st.session_state["workout_started"] = True
                st.session_state["set_cycle_start_time"] = time.time()
                st.session_state["last_saved_set_completed_at"] = 0

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_started",
                        exercise=plan_exercise,
                        metrics={}
                    )

                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.success(f"Started {plan_exercise} workout plan!")
                st.rerun()  # Rerun to update the session state and show the main content
        else:
            st.markdown("### Workout in Progress")
            exercise = st.session_state.get("plan_exercise")
            sets = st.session_state.get("plan_sets")
            reps = st.session_state.get("plan_reps")
            st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")

            stop_workout_button = st.button("Stop Workout", key="stop_workout", width="stretch")
            if stop_workout_button:
                st.session_state["workout_started"] = False
                st.success("Workout stopped. Great job!")

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_completed",
                        exercise=exercise,
                        metrics={}
                    )
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.rerun()  # Rerun to update the session state and show the main content

            # Display real-time metrics
            st.divider()
            st.subheader("Progress")

            exercise = st.session_state.get("plan_exercise")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")
            reps_per_set = st.session_state.get("plan_reps")
            sets_completed = st.session_state.get("sets_completed")
            target_sets = st.session_state.get("plan_sets")

            # Progress metrics in a compact 3-column layout
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Reps", f"{total_reps}")
            
            with col2:
                current_set_progress = current_set_reps / reps_per_set if reps_per_set > 0 else 0
                st.metric("Set Reps", f"{current_set_reps}/{reps_per_set}")
                st.progress(min(current_set_progress, 1.0))
            
            with col3:
                sets_progress = sets_completed / target_sets if target_sets > 0 else 0
                st.metric("Sets", f"{sets_completed}/{target_sets}")
                st.progress(min(sets_progress, 1.0))

            st.divider()

            if exercise == "Squats":
                st.subheader("Squat Metrics")
                
                knee_angle = st.session_state.knee_angle
                back_angle = st.session_state.back_angle
                depth_angle = st.session_state.front_knee_angle
                depth_status = st.session_state.depth_status
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Knee", f"{knee_angle}°")
                    st.caption("Ideal: 70-90°")
                    if knee_angle != 0:
                        knee_progress = min(knee_angle / 100, 1.0)
                        st.progress(knee_progress)
                
                with col2:
                    st.metric("Back", f"{back_angle}°")
                    st.caption("Ideal: 30-45°")
                    if back_angle != 0:
                        back_progress = min(back_angle / 50, 1.0)
                        st.progress(back_progress)
                
                with col3:
                    st.metric("Depth", f"{depth_angle}°")
                    st.caption(f"{depth_status} — Ideal depth angle range")
                    if depth_angle != 0:
                        depth_progress = min(depth_angle / 100, 1.0)
                        st.progress(depth_progress)
            elif exercise == "Shoulder Press":
                st.subheader("Shoulder Press Metrics")
                
                elbow_angle = st.session_state.elbow_angle
                extension_status = st.session_state.extension_status
                back_arch_status = st.session_state.back_arch_status
                
                col1, col2 = st.columns([1, 1.5])
                
                with col1:
                    st.metric("Elbow", f"{elbow_angle}°")
                    st.caption("Arm extension")
                    if elbow_angle != 0:
                        elbow_progress = min(elbow_angle / 180, 1.0)
                        st.progress(elbow_progress)
                
                with col2:
                    st.markdown("**Extension**")
                    st.write(extension_status)
                    st.caption("Press stage")
                    st.markdown("**Back Arch**")
                    st.write(back_arch_status)
                    st.caption("Spine alignment")
