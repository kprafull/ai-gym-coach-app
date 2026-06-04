import importlib

import pytest

from core.base_exercise import BaseExercise


def test_app_imports() -> None:
    importlib.import_module("app")


def test_get_angle_returns_right_angle() -> None:
    class DummyExercise(BaseExercise):
        def process(self, landmarks):
            pass

        def reset(self):
            pass

    exercise = DummyExercise()
    angle = exercise.get_angle((1, 0), (0, 0), (0, 1))
    assert angle == pytest.approx(90.0, rel=1e-3)
