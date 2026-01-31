import numpy as np
from utils.geometry import calculate_angle

class LateralRaise:
    def __init__(self, side='left'):
        self.side = side
        self.counter = 0
        self.stage = None
        self.feedback = ""

    def process(self, lmList, w, h):
        if not lmList:
            return None

        # Left: 11 (shoulder), 13 (elbow), 15 (wrist) + 23 (hip)
        if self.side == 'left':
            hip = [lmList[23][1], lmList[23][2]]
            shoulder = [lmList[11][1], lmList[11][2]]
            elbow = [lmList[13][1], lmList[13][2]]
            wrist = [lmList[15][1], lmList[15][2]]
        else:
            hip = [lmList[24][1], lmList[24][2]]
            shoulder = [lmList[12][1], lmList[12][2]]
            elbow = [lmList[14][1], lmList[14][2]]
            wrist = [lmList[16][1], lmList[16][2]]

        # Angle 1: Elbow straightness (Shoulder-Elbow-Wrist)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        
        # Angle 2: Arm height (Hip-Shoulder-Elbow)
        shoulder_angle = calculate_angle(hip, shoulder, elbow)

        feedback = ""
        
        # Check Elbow Straightness
        if elbow_angle < 150:
             feedback += "Straighten Arms! "
        
        # Check Height
        if shoulder_angle > 80 and shoulder_angle < 100:
            if self.stage != "up":
                self.stage = "up"
                self.counter += 1
                feedback = "Good Height!"
        elif shoulder_angle < 30:
            self.stage = "down"

        return {
            "angle": shoulder_angle, # Monitoring lift angle
            "elbow_angle": elbow_angle,
            "count": self.counter,
            "stage": self.stage,
            "feedback": feedback,
            "joints": (hip, shoulder, elbow)
        }
