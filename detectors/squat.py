from core.base_exercise import BaseExercise

class SquatDetector(BaseExercise):
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    def __init__(self):
        super().__init__()

    def process(self, landmarks):
        if not landmarks:
            return None
        
        left_vis = landmarks[self.LEFT_KNEE].visibility # left knee visibility
        right_vis = landmarks[self.RIGHT_KNEE].visibility # right knee visibility

        if left_vis <= right_vis:
            knee_angle = int(self.get_angle(
                self.get_point(landmarks, self.LEFT_HIP),
                self.get_point(landmarks, self.LEFT_KNEE),
                self.get_point(landmarks, self.LEFT_ANKLE)
            ))
            hip_idx, knee_idx, ankle_idx, shoulder_idx = self.LEFT_HIP, self.LEFT_KNEE, self.LEFT_ANKLE, self.LEFT_SHOULDER
        else:
            knee_angle = int(self.get_angle(
                self.get_point(landmarks, self.RIGHT_HIP),
                self.get_point(landmarks, self.RIGHT_KNEE),
                self.get_point(landmarks, self.RIGHT_ANKLE)
            ))
            hip_idx, knee_idx, ankle_idx, shoulder_idx = self.RIGHT_HIP, self.RIGHT_KNEE, self.RIGHT_ANKLE, self.RIGHT_SHOULDER

        back_angle = int(self.get_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, knee_idx)
        ))

        key_landmkars_visible = all(landmarks[idx].visibility > 0.7 for idx in [hip_idx, knee_idx, ankle_idx, shoulder_idx])
        if key_landmkars_visible:
            if knee_angle < 100:
                self.stage = "down"

            if knee_angle > 160 and self.stage == "down":
                self.stage = "up"
                self.reps += 1

            if self.stage == "down":
                if knee_angle < 70:
                    self.depth_status = "Too Deep"
                elif knee_angle < 100:
                    self.depth_status = "Good Depth"
                else:
                    self.depth_status = "Too High"
            elif self.stage == "up":
                self.depth_status = "Standing"
            else:       
                self.depth_status = "No Detection"

            return {
                "reps": self.reps,
                "knee_angle": knee_angle,
                "back_angle": back_angle,
                "depth_status": self.depth_status
            }

    def reset(self):
        self.reps = 0
        self.stage = None
