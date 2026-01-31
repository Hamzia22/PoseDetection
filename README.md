# AI Fitness Trainer - Form Correctness Detection

This project uses **MediaPipe** and **OpenCV** to build a form correction pipeline for exercises. It tracks body keypoints to analyze posture and provides real-time feedback.

## Features
- **Bicep Curl**: Monitors elbow extension and contraction.
- **Squat**: Tracks hip depth relative to knees.
- **Lateral Raise**: Ensures arms are straight and lifted to shoulder height.
- **Real-time Feedback**: Visual overlays for reps, stage (up/down), and form corrections.

## Setup

## Setup

1. **Create and Activate Virtual Environment** (Required on macOS):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
   
   *Alternatively, you can run `bash setup_env.sh` to do this automatically.*

3. **Download Model File**:
   The application requires the MediaPipe Pose Landmarker model. The setup script downloads this to `utils/pose_landmarker_heavy.task`.
   If you set up manually, download it:
   ```bash
   curl -o utils/pose_landmarker_heavy.task https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task
   ```

## Usage

**Important**: Always ensure your virtual environment is active (`source venv/bin/activate`) before running the script.

Run the `main.py` script. You can specify the exercise, video source, and side (left/right).

### Arguments
- `--exercise`: `curl` (default), `squat`, or `raise`.
- `--source`: Path to video file or `0` for webcam (default).
- `--side`: `left` (default) or `right`.

### Examples

**1. Run Bicep Curl on Webcam:**
```bash
python3 main.py --exercise curl
```

**2. Run Squat Analysis on a Video File:**
```bash
python3 main.py --exercise squat --source path/to/video.mp4 --side right
```

**3. Run Lateral Raise Analysis:**
```bash
python3 main.py --exercise raise
```

### Batch Processing
You can process an entire folder of videos and save the results.
```bash
python3 main.py --exercise curl --source path/to/video_folder --output path/to/results --no-display
```
- `--source`: Path to folder containing videos.
- `--output`: Path to folder where analyzed videos and logs will be saved.
- `--no-display`: (Optional) Runs faster by hiding the window.

## Key Controls
- Press **'q'** to quit the application.
