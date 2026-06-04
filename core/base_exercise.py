from abc import ABC, abstractmethod
import numpy as np
import math

class BaseExercise(ABC):
    def __init__(self):
        self.reps = 0
        self.stage = None

    @abstractmethod
    def process(self, landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass

    def get_point(self, landmarks, index):
        p = landmarks[index]
        return (p.x, p.y)
    
    def get_angle(self, a, b, c):
        ax, ay = a[0] - b[0], a[1] - b[1]
        cx, cy = c[0] - b[0], c[1] - b[1]
        dot = ax * cx + ay * cy
        norm_a = math.sqrt(ax * ax + ay * ay)
        norm_c = math.sqrt(cx * cx + cy * cy)
        if norm_a == 0 or norm_c == 0:
            return 0.0
        cos_angle = dot / (norm_a * norm_c)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = math.degrees(math.acos(cos_angle))

        return angle