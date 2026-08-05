import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT_CORNER = 33
LEFT_EYE_RIGHT_CORNER = 133
EAR_THRESHOLD = 0.23


def calculate_ear(face_landmarks, frame_width, frame_height):
    """
    Calculates Eye Aspect Ratio (EAR) for the left eye.
    Drops sharply during a blink, recovers once eye reopens.
    """
    top = face_landmarks.landmark[LEFT_EYE_TOP]
    bottom = face_landmarks.landmark[LEFT_EYE_BOTTOM]
    left_corner = face_landmarks.landmark[LEFT_EYE_LEFT_CORNER]
    right_corner = face_landmarks.landmark[LEFT_EYE_RIGHT_CORNER]

    top_y = top.y * frame_height
    bottom_y = bottom.y * frame_height
    vertical_gap = abs(bottom_y - top_y)

    left_x = left_corner.x * frame_width
    right_x = right_corner.x * frame_width
    horizontal_width = abs(right_x - left_x)

    if horizontal_width > 0:
        ear = vertical_gap / horizontal_width
    else:
        ear = 0.0

    return ear


def analyze_blink_rate(video_filepath, fps=20):
    """
    Detects blink EVENTS (closed-to-open transitions) and calculates
    blinks per minute across the video.
    """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None

    print(f"\n  😉 Analyzing blink rate: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_blinks = 0
    total_scored_frames = 0
    eye_was_closed = False

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                face_landmarks = results.multi_face_landmarks[0]
                ear = calculate_ear(face_landmarks, frame_width, frame_height)

                total_scored_frames += 1

                if ear < EAR_THRESHOLD:
                    eye_was_closed = True
                else:
                    if eye_was_closed:
                        total_blinks += 1
                    eye_was_closed = False

    cap.release()

    if total_scored_frames > 0:
        duration_minutes = (total_scored_frames / fps) / 60
        blinks_per_minute = round(total_blinks / duration_minutes, 1) if duration_minutes > 0 else 0.0
    else:
        blinks_per_minute = 0.0

    print(f"  ✓ Total blinks detected : {total_blinks}")
    print(f"  ✓ Blink rate            : {blinks_per_minute} blinks/min")

    return {
         'total_blinks': total_blinks,
        'blinks_per_minute': blinks_per_minute,
        'total_scored_frames': total_scored_frames
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_blink_rate(filepath)