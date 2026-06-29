# core/video_recorder.py
# Responsibility: record webcam video and save as AVI file
# Used by: main.py

import cv2        # opencv — captures webcam frames
import os         # creating folders, building file paths

# Constants — values that don't change during recording
FPS = 20          # frames per second — 20 captures per second
OUTPUT_DIR = "output"  # same folder as audio files

def record_video(duration=10, filename_timestamp=None):
    """
    Records webcam video and saves it as an AVI file.

    Parameters:
        duration (int): how many seconds to record. Default 10.
        filename_timestamp (str): timestamp string for naming the file.
                                  If None, generates its own timestamp.

    Returns:
        str: filepath of the saved video file.
    """

    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build filename using the shared timestamp
    # We use the same timestamp as audio so both files match
    if filename_timestamp is None:
        from datetime import datetime
        filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # os.path.join() builds file paths in an OS-independent way
    # (Windows uses '\' while Linux/macOS use '/')
    filename = f"session_{filename_timestamp}.avi"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Open the webcam
    # 0 means the default camera — your built-in webcam
    # If you have multiple cameras, try 1 or 2
    cap = cv2.VideoCapture(0)

    # Check if webcam opened successfully
    if not cap.isOpened():
        print("  ✗ Error: Could not open webcam.")
        print("  Check that your webcam is connected and not used by another app.")
        return None

    # Get the actual frame width and height from your webcam
    # We ask the webcam what resolution it supports
    # rather than hardcoding a size that might not match
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set up the video writer — this saves frames to a file
    # cv2.VideoWriter_fourcc sets the video codec (compression format)
    # 'XVID' is a widely supported codec that works on Windows and Mac
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filepath, fourcc, FPS, (frame_width, frame_height))

    print("  📹 Webcam recording started...")

    # Calculate total frames to capture
    # 10 seconds x 20 FPS = 200 frames total
    total_frames = duration * FPS
    frames_captured = 0

    # Keep capturing frames until we hit the total
    while frames_captured < total_frames:

        # Read one frame from the webcam
        # ret = True if frame was read successfully, False if webcam failed
        # frame = the actual image data as a numpy array
        ret, frame = cap.read()

        if not ret:
            print("  ✗ Warning: Failed to read frame from webcam.")
            break

        # Write this frame to the video file
        out.write(frame)
        frames_captured += 1

    # Always release resources when done
    # cap.release() closes the webcam connection
    # out.release() finalizes and closes the video file
    cap.release()
    out.release()

    print(f"  ✓ Video saved to: {filepath}")
    # Return the filepath so it can be used by the next stage of the pipeline.
    return filepath


# Test block — only runs when you execute this file directly
if __name__ == "__main__":
    print("Testing video recorder...")
    saved_path = record_video(duration=5)
    if saved_path:
        print(f"\nTest complete. File saved at: {saved_path}")
        print("Open the output/ folder and play the AVI file to verify.")