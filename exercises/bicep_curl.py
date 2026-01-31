import numpy as np
from utils.geometry import calculate_angle

class BicepCurl:
    def __init__(self, side='left'):
        self.side = side
        self.counter = 0
        self.stage = None # 'up' or 'down'
        self.feedback = ""

    def process(self, lmList, w, h):
        if not lmList:
            return None

        # Landmarks for Left arm: 11, 13, 15
        # Landmarks for Right arm: 12, 14, 16
        if self.side == 'left':
            shoulder = [lmList[11][1], lmList[11][2]]
            elbow = [lmList[13][1], lmList[13][2]]
            wrist = [lmList[15][1], lmList[15][2]]
        else:
            shoulder = [lmList[12][1], lmList[12][2]]
            elbow = [lmList[14][1], lmList[14][2]]
            wrist = [lmList[16][1], lmList[16][2]]

        # Calculate Angle
        angle = calculate_angle(shoulder, elbow, wrist)

        # Logic
        # Relaxed thresholds for easier detection
        if angle > 145:
            self.stage = "down"
        if angle < 60 and self.stage == 'down':
            self.stage = "up"
            self.counter += 1
            self.feedback = "Good Rep!"
        elif angle < 60 and self.stage == 'up':
            self.feedback = "Lower arm fully"
        
        return {
            "angle": angle,
            "count": self.counter,
            "stage": self.stage,
            "feedback": self.feedback,
            "joints": (shoulder, elbow, wrist)
        }
