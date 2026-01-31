import mediapipe as mp
import cv2
import numpy as np
import os

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        
        # New API doesn't map parameters 1:1, but we can set Options.
        base_options = python.BaseOptions(model_asset_path='utils/pose_landmarker_heavy.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=enable_segmentation,
            min_pose_detection_confidence=detectionCon,
            min_pose_presence_confidence=detectionCon,
            min_tracking_confidence=trackCon,
            # running_mode=vision.RunningMode.VIDEO 
            # We will use IMAGE mode for simplicity in the loop unless we need tracking benefits
            # VIDEO mode requires timestamps. Let's use VIDEO for better tracking if possible, 
            # but IMAGE is safer to implement quickly without managing execution order/timestamps perfectly.
            # Actually, standard loop uses VIDEO logic implicitly. 
            running_mode=vision.RunningMode.VIDEO
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)
        self.results = None
        
        # Helper for drawing - Tasks API doesn't have a simple "draw_landmarks" attached
        # We need to use mp.solutions.drawing_utils if available, OR generic drawing.
        # But wait, mp.solutions IS MISSING.
        # We will implement custom drawing in findPose or Main.
        
    def findPose(self, img, timestamp_ms, draw=True):
        # Image needs to be MP Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Detect for VIDEO
        self.results = self.detector.detect_for_video(mp_image, timestamp_ms)

        if draw and self.results.pose_landmarks:
             # Basic custom drawing since mp.solutions is gone
             for landmarks in self.results.pose_landmarks:
                 for lm in landmarks:
                     h, w, c = img.shape
                     cx, cy = int(lm.x * w), int(lm.y * h)
                     cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                     
                 # Draw connections if needed, but main.py handles specific skeleton drawing
                 # We can rely on main.py for skeleton
        
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results and self.results.pose_landmarks:
            # We assume single person for now
            myLandmarks = self.results.pose_landmarks[0]
            for id, lm in enumerate(myLandmarks):
                h, w, c = img.shape
                # cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, lm.x, lm.y, lm.z, lm.visibility])
        return self.lmList
