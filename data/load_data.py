import pandas as pd


def get_sample_data() -> pd.DataFrame:
    """Return a small sample DataFrame for the app."""
    return pd.DataFrame(
        {
            "exercise": ["Squat", "Bench Press", "Deadlift", "Pull-up"],
            "sets": [3, 4, 3, 3],
            "reps": [8, 6, 5, 10],
            "weight": [100, 80, 140, 0],
        }
    )
