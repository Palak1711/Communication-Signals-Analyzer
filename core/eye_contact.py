import cv2
import mediapipe as mp
import os
import math

from core.eye_tracker import (
    get_eye_coordinates,
    calculate_eye_center,
    LEFT_EYE_INDICES,
    RIGHT_EYE_INDICES
)

mp_face_mesh = mp.solutions.face_mesh

CALIBRATION_SECONDS = 3
EYE_CONTACT_THRESHOLD_RATIO = 0.04  # 4% of frame width


def calculate_distance(point1, point2):
    """Euclidean distance between two (x, y) points."""
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def get_gaze_point(face_landmarks, frame_width, frame_height):
    """Averages both eyes into one overall gaze point."""
    left_coords = get_eye_coordinates(face_landmarks, LEFT_EYE_INDICES, frame_width, frame_height)
    right_coords = get_eye_coordinates(face_landmarks, RIGHT_EYE_INDICES, frame_width, frame_height)

    left_center = calculate_eye_center(left_coords)
    right_center = calculate_eye_center(right_coords)

    gaze_x = (left_center[0] + right_center[0]) / 2
    gaze_y = (left_center[1] + right_center[1]) / 2

    return (gaze_x, gaze_y)


def analyze_eye_contact(video_filepath, fps=20):
    """
    Calibrates a personal gaze baseline from the first few seconds,
    then measures eye contact percentage for the rest of the video.
    """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None

    print(f"\n  👁  Analyzing eye contact: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    threshold = frame_width * EYE_CONTACT_THRESHOLD_RATIO
    calibration_frame_count = CALIBRATION_SECONDS * fps

    calibration_points = []
    eye_contact_flags = []
    frame_num = 0
    baseline = None

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                face_landmarks = results.multi_face_landmarks[0]
                gaze_point = get_gaze_point(face_landmarks, frame_width, frame_height)

                if frame_num <= calibration_frame_count:
                    calibration_points.append(gaze_point)
                else:
                    if baseline is None and calibration_points:
                        baseline_x = sum(p[0] for p in calibration_points) / len(calibration_points)
                        baseline_y = sum(p[1] for p in calibration_points) / len(calibration_points)
                        baseline = (baseline_x, baseline_y)
                        print(f"  ✓ Calibration complete. Baseline: ({baseline[0]:.1f}, {baseline[1]:.1f})")

                    if baseline is not None:
                        distance = calculate_distance(gaze_point, baseline)
                        is_eye_contact = distance < threshold
                        eye_contact_flags.append(is_eye_contact)

    cap.release()

    total_scored_frames = len(eye_contact_flags)
    frames_with_contact = sum(eye_contact_flags)

    if total_scored_frames > 0:
        eye_contact_percentage = round((frames_with_contact / total_scored_frames) * 100, 1)
    else:
        eye_contact_percentage = 0.0

    print(f"  ✓ Eye contact: {eye_contact_percentage}% ({frames_with_contact}/{total_scored_frames} scored frames)")

    return {
        'eye_contact_percentage': eye_contact_percentage,
        'frames_with_contact': frames_with_contact,
        'total_scored_frames': total_scored_frames
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_eye_contact(filepath)