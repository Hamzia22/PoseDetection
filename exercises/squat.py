import numpy as np
from utils.geometry import calculate_angle

class Squat:
    def __init__(self, side='left'):
        self.side = side
        self.counter = 0
        self.stage = None
        self.feedback = ""

    def process(self, lmList, w, h):
        if not lmList:
            return None
        
        # Left: 23 (hip), 25 (knee), 27 (ankle)
        # Right: 24, 26, 28
        if self.side == 'left':
            hip = [lmList[23][1], lmList[23][2]]
            knee = [lmList[25][1], lmList[25][2]]
            ankle = [lmList[27][1], lmList[27][2]]
        else:
            hip = [lmList[24][1], lmList[24][2]]
            knee = [lmList[26][1], lmList[26][2]]
            ankle = [lmList[28][1], lmList[28][2]]

        angle = calculate_angle(hip, knee, ankle)
        
        if angle > 170:
            self.stage = "up"
        if angle < 90 and self.stage == "up":
            self.stage = "down"
            self.counter += 1
            self.feedback = "Good Depth!"
        elif angle < 90:
             self.feedback = "Good Depth!"
        elif angle > 90 and angle < 140 and self.stage == "down":
             self.feedback = "Go Lower"

        return {
            "angle": angle,
            "count": self.counter,
            "stage": self.stage,
            "feedback": self.feedback,
            "joints": (hip, knee, ankle)
        }
