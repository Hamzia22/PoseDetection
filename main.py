import cv2
import argparse
import time
import numpy as np
import os
import sys

from utils.pose_module import PoseDetector
from exercises.bicep_curl import BicepCurl
from exercises.squat import Squat
from exercises.lateral_raise import LateralRaise

def process_video(source_path, output_dir, exercise_type, side, no_display=False):
    """
    Process a single video source and save results to output_dir (if provided).
    Returns a dictionary of stats.
    """
    
    # Determine input type
    is_camera = str(source_path).isdigit()
    if is_camera:
        cap = cv2.VideoCapture(int(source_path))
        input_name = "camera"
    else:
        cap = cv2.VideoCapture(source_path)
        input_name = os.path.splitext(os.path.basename(source_path))[0]
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {source_path}")
        return None

    # Determine Output Paths
    video_writer = None
    log_file = None
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        # Video Output
        save_path = os.path.join(output_dir, f"{input_name}_analyzed.mp4")
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30 # Default if unknown
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID'
        video_writer = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        
        # Log Output
        log_path = os.path.join(output_dir, f"{input_name}_log.txt")
        log_file = open(log_path, 'w')
        log_file.write(f"Analysis Log for {input_name}\n")
        log_file.write(f"Exercise: {exercise_type}, Side: {side}\n")
        log_file.write(f"{'-'*30}\n")
    
    # Initialize Detector & Exercise
    detector = PoseDetector()
    if exercise_type == 'curl':
        exercise = BicepCurl(side=side)
    elif exercise_type == 'squat':
        exercise = Squat(side=side)
    elif exercise_type == 'raise':
        exercise = LateralRaise(side=side)
    
    print(f"Processing: {input_name}...")
    
    pTime = 0
    frame_count = 0
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        frame_count += 1
        h, w, c = img.shape
        timestamp_ms = int(time.time() * 1000) # Or frame_count / fps * 1000 for strict video time

        # 1. Find Pose
        img = detector.findPose(img, timestamp_ms, draw=False) 
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # 2. Process Exercise
            data = exercise.process(lmList, w, h)
            
            if data:
                # Log relevant events
                if log_file and data.get('feedback'):
                     # Simple log throttling: only log if state changed or error
                     # For now, let's log every rep completion
                     if "Good" in data['feedback'] and data.get('stage') == 'up' and exercise_type == 'curl': 
                         # This logic is imperfect for generic logging, but suffices for a summary.
                         pass
                
                # 3. Visualization
                joints = data.get('joints', [])
                if len(joints) >= 3:
                     p1 = (int(joints[0][0] * w), int(joints[0][1] * h))
                     p2 = (int(joints[1][0] * w), int(joints[1][1] * h))
                     p3 = (int(joints[2][0] * w), int(joints[2][1] * h))
                     
                     cv2.line(img, p1, p2, (255, 255, 255), 3)
                     cv2.line(img, p2, p3, (255, 255, 255), 3)
                     cv2.circle(img, p1, 10, (0, 0, 255), cv2.FILLED)
                     cv2.circle(img, p2, 10, (0, 0, 255), cv2.FILLED)
                     cv2.circle(img, p3, 10, (0, 0, 255), cv2.FILLED)

                # UI Overlay
                # Increase box size slightly
                cv2.rectangle(img, (0, 0), (300, 150), (0, 0, 0), cv2.FILLED)
                
                # Count
                cv2.putText(img, f'Reps: {int(data["count"])}', (10, 50), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                
                # Stage
                if data['stage']:
                    cv2.putText(img, f'Stage: {data["stage"]}', (10, 90), 
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                
                # Feedback
                if data['feedback']:
                    color = (0, 255, 0) if "Good" in data['feedback'] else (0, 0, 255)
                    cv2.putText(img, data['feedback'], (10, 130), 
                                cv2.FONT_HERSHEY_PLAIN, 1.5, color, 2)

        # FPS
        cTime = time.time()
        fps_disp = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps_disp)}', (w - 150, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Write to video
        if video_writer:
            video_writer.write(img)

        # Display
        if not no_display:
            cv2.imshow("AI Trainer", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Cleanup
    cap.release()
    if video_writer:
        video_writer.release()
    if log_file:
        log_file.write(f"\nFinal Stats:\n")
        log_file.write(f"Total Reps: {exercise.counter}\n")
        log_file.close()
    if not no_display:
        cv2.destroyAllWindows()
        
    return {"reps": exercise.counter}

def main():
    parser = argparse.ArgumentParser(description='AI Fitness Trainer')
    parser.add_argument('--exercise', type=str, default='curl', 
                        choices=['curl', 'squat', 'raise'],
                        help='Exercise type')
    parser.add_argument('--source', type=str, default='0',
                        help='Video source: 0, path to file, or path to FOLDER')
    parser.add_argument('--side', type=str, default='left',
                        choices=['left', 'right'],
                        help='Side of body')
    parser.add_argument('--output', type=str, default=None,
                        help='Directory to save results (videos/logs)')
    parser.add_argument('--no-display', action='store_true',
                        help='Run without showing video window')

    args = parser.parse_args()

    # Check if directory
    if os.path.isdir(args.source):
        print(f"Batch processing folder: {args.source}")
        files = [f for f in os.listdir(args.source) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        
        if not files:
            print("No video files found in folder.")
            return

        for f in files:
            full_path = os.path.join(args.source, f)
            print(f"Starting {f}...")
            process_video(full_path, args.output, args.exercise, args.side, args.no_display)
            
    else:
        # Single file
        process_video(args.source, args.output, args.exercise, args.side, args.no_display)

if __name__ == "__main__":
    main()
