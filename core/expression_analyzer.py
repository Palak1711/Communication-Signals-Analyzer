import cv2
import mediapipe as mp
import os
import math

mp_face_mesh = mp.solutions.face_mesh

UPPER_LIP_INDEX = 13
LOWER_LIP_INDEX = 14
LEFT_MOUTH_CORNER_INDEX = 61
RIGHT_MOUTH_CORNER_INDEX = 291


def get_mouth_openness_ratio(face_landmarks, frame_width, frame_height):
    """
    Calculates mouth openness as vertical gap divided by mouth width -
    a ratio, so it stays meaningful regardless of camera distance.
    """
    upper = face_landmarks.landmark[UPPER_LIP_INDEX]
    lower = face_landmarks.landmark[LOWER_LIP_INDEX]
    left_corner = face_landmarks.landmark[LEFT_MOUTH_CORNER_INDEX]
    right_corner = face_landmarks.landmark[RIGHT_MOUTH_CORNER_INDEX]
    
    upper_y = upper.y * frame_height
    lower_y = lower.y * frame_height
    vertical_gap = abs(lower_y - upper_y)

    left_x = left_corner.x * frame_width
    right_x = right_corner.x * frame_width
    mouth_width = abs(right_x - left_x)

    if mouth_width > 0:
        ratio = vertical_gap / mouth_width
    else:
        ratio = 0.0

    return ratio


def calculate_expressiveness_score(ratios):
    """Manually calculates standard deviation of a list of ratios."""
    if len(ratios) < 2:
        return 0.0

    mean_ratio = sum(ratios) / len(ratios)

    squared_diffs = [(r - mean_ratio) ** 2 for r in ratios]
    variance = sum(squared_diffs) / len(squared_diffs)
    std_dev = math.sqrt(variance)

    return std_dev


def variation_to_score(std_dev):
    """Converts expressiveness variation into a 0-100 score."""
    if std_dev < 0.02:
        return 30
    elif std_dev < 0.05:
        return 60
    elif std_dev < 0.10:
        return 90
    else:
        return 75


def analyze_facial_expression(video_filepath):
    """
    Tracks mouth openness ratio across every frame and calculates
    how much it varies - a proxy for facial expressiveness.
    """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None

    print(f"\n  🙂 Analyzing facial expression: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    mouth_ratios = []

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                face_landmarks = results.multi_face_landmarks[0]
                ratio = get_mouth_openness_ratio(face_landmarks, frame_width, frame_height)
                mouth_ratios.append(ratio)

    cap.release()

    std_dev = calculate_expressiveness_score(mouth_ratios)
    expression_score = variation_to_score(std_dev)

    print(f"  ✓ Mouth openness variation : {round(std_dev, 4)}")
    print(f"  ✓ Expressiveness score      : {expression_score}/100")

    return {
        'mouth_variation': round(std_dev, 4),
        'expression_score': expression_score,
        'frames_analyzed': len(mouth_ratios)
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_facial_expression(filepath)