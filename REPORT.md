# Form Correctness Detection Report

## 1. Posture Rules Used & Logic

### A. Bicep Curl
**Objective**: Ensure full range of motion.
- **Keypoints Tracked**: Shoulder, Elbow, Wrist (11, 13, 15 for left; 12, 14, 16 for right).
- **Metric**: Elbow Angle (Angle at Elbow vertex formed by Shoulder and Wrist).
- **Rules**:
    1.  **Extension (Down)**: Angle > 145°. Indicates the arm is fully engaged at the bottom.
    2.  **Contraction (Up)**: Angle < 60°. Indicates a full curl.
    3.  **Feedback**: "Lower arm fully" if the user curls up without fully extending first.

### B. Squat
**Objective**: Ensure proper depth (thighs parallel to ground).
- **Keypoints Tracked**: Hip, Knee, Ankle (23, 25, 27 for left).
- **Metric**: Knee Angle (Angle at Knee vertex formed by Hip and Ankle).
- **Rules**:
    1.  **Standing (Up)**: Angle > 170°.
    2.  **Squat Depth (Down)**: Angle < 90°. This generally indicates thighs are parallel or below parallel.
    3.  **Feedback**: "Go Lower" if the user starts ascending before reaching < 90°. "Good Depth" when threshold is met.

### C. Lateral Raise
**Objective**: maintain straight arms and proper shoulder height.
- **Keypoints Tracked**: Hip, Shoulder, Elbow, Wrist.
- **Metric 1**: Elbow Angle (Arm Straightness).
- **Metric 2**: Shoulder Angle (Elevation relative to Hip-Shoulder line).
- **Rules**:
    1.  **Arm Straightness**: Elbow Angle should be > 150°. If less, feedback "Straighten Arms!" is shown.
    2.  **Height**: Shoulder Angle (Hip-Shoulder-Elbow) should range between 80-100° at the top.
    3.  **Feedback**: "Good Height" when in range.

## 2. Methodology
- **Pose Estimation**: Used **MediaPipe Pose** soluton. It is lightweight, robust, and provides 33 3D landmarks.
- **Smoothing**: MediaPipe's built-in `smooth_landmarks=True` parameter was enabled to reduce jitter.
- **Geometry**: Custom utility to calculate 2D angles using `arctan2`. This is robust against gimbal lock issues generally faced in 3D but sufficient for 2D plane analysis.
- **State Machine**: Simple state machines (Up/Down) are used to count reps only when a full cycle of motion is completed, preventing cheat reps.

## 3. Challenges & Future Improvements
1.  **Occlusion**: If the camera angle is not optimal (e.g., side view for squats is best), keypoints may be occluded.
    - *Solution*: I added a `--side` argument to switch between tracking left or right body parts effectively.
2.  **Multiple Persons**: The current implementation assumes a single primary user. MediaPipe Pose is largely a single-person model.
    - *Future Solution*: To handle multiple persons, we would need to use an object detection model (like YOLO) to detect person bounding boxes first, and then run the Pose model on each cropped person ensuring ID tracking.
3.  **Z-axis depth**: 2D angles can be misleading if the user is facing the camera directly for exercises that require a side view (like squats).
    - *Mitigation*: The instructions/README implies proper camera positioning. 3D landmark data from MediaPipe (z-coordinate) could be used to correct or warn the user about their orientation.
