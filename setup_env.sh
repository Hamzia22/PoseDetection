#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Download MediaPipe Model
echo "Downloading MediaPipe Pose Model..."
curl -o utils/pose_landmarker_heavy.task https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task

echo "Setup complete! To run the app use:"
echo "source venv/bin/activate"
echo "python3 main.py --exercise curl"
