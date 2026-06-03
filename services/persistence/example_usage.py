"""
Example usage of SQLite-based ExerciseRepository.

This module demonstrates how to use the exercise repository for storing
and retrieving workout data.
"""

from services.persistence.exercise_repository import ExerciseRepository


def example_basic_operations():
    """Example: Basic repository operations."""
    repo = ExerciseRepository()
    
    # Add exercises
    squat_id = repo.add_exercise("Squats", "Lower body compound exercise")
    bench_id = repo.add_exercise("Bench Press", "Upper body compound exercise")
    
    # Get all exercises
    exercises = repo.get_all_exercises()
    print(f"Exercises in database: {exercises}")
    
    # Start a workout session
    session_id = repo.start_workout_session(
        user_id="user_123",
        exercise_name="Squats",
        sets=4,
        reps=8,
        notes="Heavy day"
    )
    print(f"Started workout session: {session_id}")
    
    # Add metrics during the workout
    repo.add_metric(session_id, "knee_angle", 85.5)
    repo.add_metric(session_id, "back_angle", 35.2)
    repo.add_metric(session_id, "depth_status", 90)  # Representing "Good" as numeric
    
    # Get metrics from session
    metrics = repo.get_session_metrics(session_id)
    print(f"Session metrics: {metrics}")
    
    # End the workout session
    repo.end_workout_session(session_id)
    
    # Get user's recent sessions
    user_sessions = repo.get_user_sessions("user_123")
    print(f"User sessions: {user_sessions}")


def test_get_user(user_name: str = "user123"):
    """Quick test helper for verifying get_user() returns data for a user.

    Prints a short summary and returns the list for further assertions.
    """
    repo = ExerciseRepository()
    user = repo.get_user(user_name)
    if not user:
        print(f"No user found with username '{user_name}'.")
    else:
        print(f"Found user '{user_name}':")
        for key, value in user.items():
            print(f" - {key}: {value}")

    return user

def test_add_exercise():
    """Quick test helper for verifying add_exercise() adds an exercise.

    Prints a short summary and returns the exercise ID for further assertions.
    """
    repo = ExerciseRepository()
    exercise_id = repo.add_exercise("user_123", "Test Exercise", 10, 3, 60)
    print(f"Added exercise for user 'user_123' with ID {exercise_id}.")

    # Verify it was added
    exercises = repo.get_user_exercises("user_123")
    added_exercise = next((ex for ex in exercises if ex["id"] == exercise_id), None)
    if added_exercise:
        print(f"Verified exercise: {added_exercise}")
    else:
        print(f"Failed to verify exercise with ID {exercise_id}.")

    return exercise_id

def test_create_user(username: str, hashed_password: str):
    """Quick test helper for creating a user and verifying it was created."""
    repo = ExerciseRepository()
    user_id = repo.create_user(username, hashed_password)
    print(f"Created user '{username}' with ID {user_id}.")
    
    # Verify the user can be retrieved
    user = repo.get_user(username)
    if user:
        print(f"Verified user retrieval: {user}")
    else:
        print(f"Failed to retrieve user '{username}' after creation.")
    
    return user

if __name__ == "__main__":
    # example_basic_operations()
    test_create_user("testuser", "hashedpassword123")
    test_get_user("testuser")
    test_add_exercise()