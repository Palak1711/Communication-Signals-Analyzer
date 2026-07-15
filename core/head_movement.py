import cv2
import mediapipe as mp
import os

from core.eye_contact import calculate_distance

mp_face_mesh = mp.solutions.face_mesh

NOSE_TIP_INDEX = 1
MOVEMENT_THRESHOLD_RATIO = 0.015  # 1.5% of frame width


def get_nose_position(face_landmarks, frame_width, frame_height):
    """Returns the nose tip's pixel (x, y) position."""
    landmark = face_landmarks.landmark[NOSE_TIP_INDEX]
    pixel_x = landmark.x * frame_width
    pixel_y = landmark.y * frame_height
    return (pixel_x, pixel_y)


def analyze_head_movement(video_filepath, fps=20):
    """
    Tracks the nose tip position frame-to-frame and counts how many
    times the head moves more than a threshold amount between
    consecutive frames.
     """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None

    print(f"\n  🧍 Analyzing head movement: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    threshold = frame_width * MOVEMENT_THRESHOLD_RATIO

    previous_position = None
    total_movements = 0
    total_scored_frames = 0

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                face_landmarks = results.multi_face_landmarks[0]
                current_position = get_nose_position(face_landmarks, frame_width, frame_height)

                if previous_position is not None:
                    distance = calculate_distance(current_position, previous_position)
                    if distance > threshold:
                        total_movements += 1
                    total_scored_frames += 1

                previous_position = current_position

    cap.release()

    if total_scored_frames > 0:
        duration_seconds = total_scored_frames / fps
        movements_per_second = round(total_movements / duration_seconds, 2)
    else:
        movements_per_second = 0.0

    print(f"  ✓ Total significant movements : {total_movements}")
    print(f"  ✓ Movement rate                : {movements_per_second} moves/sec")
    
    return {
        'total_movements': total_movements,
        'movements_per_second': movements_per_second,
        'total_scored_frames': total_scored_frames
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_head_movement(filepath)