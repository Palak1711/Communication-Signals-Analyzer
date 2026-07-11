import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE_INDICES = [263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384, 385, 386, 387, 388, 466]


def get_eye_coordinates(face_landmarks, indices, frame_width, frame_height):
    """Converts a list of landmark indices into pixel (x, y) coordinates."""
    coordinates = []
    for index in indices:
        landmark = face_landmarks.landmark[index]
        pixel_x = landmark.x * frame_width
        pixel_y = landmark.y * frame_height
        coordinates.append((pixel_x, pixel_y))
    return coordinates


def calculate_eye_center(coordinates):
    """Averages a list of (x, y) points into one center point."""
    x_values = [point[0] for point in coordinates]
    y_values = [point[1] for point in coordinates]

    center_x = sum(x_values) / len(x_values)
    center_y = sum(y_values) / len(y_values)

    return (center_x, center_y)


def analyze_eye_tracking(video_filepath):
    """
    Extracts left and right eye center coordinates from every frame
    where a face is detected. Saves one sample frame with eye
    centers marked for visual verification.
    """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None

    print(f"\n  👁  Extracting eye landmarks: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = 0
    frames_with_eyes = 0
    saved_sample = False
    sample_path = "output/eye_sample.jpg"

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            total_frames += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                face_landmarks = results.multi_face_landmarks[0]

                left_coords = get_eye_coordinates(face_landmarks, LEFT_EYE_INDICES, frame_width, frame_height)
                right_coords = get_eye_coordinates(face_landmarks, RIGHT_EYE_INDICES, frame_width, frame_height)

                left_center = calculate_eye_center(left_coords)
                right_center = calculate_eye_center(right_coords)

                print(f"  Left eye center:  {left_center}")
                print(f"  Right eye center: {right_center}")

                frames_with_eyes += 1

                if not saved_sample:
                    cv2.circle(frame, (int(right_center[0]), int(right_center[1])), 4, (0, 255, 0), -1)
                    cv2.imwrite(sample_path, frame)
                    saved_sample = True

    cap.release()

    print(f"  ✓ Frames with eyes tracked: {frames_with_eyes}/{total_frames}")
    if saved_sample:
        print(f"  ✓ Sample saved to: {sample_path}")

    return {
        'total_frames': total_frames,
        'frames_with_eyes': frames_with_eyes
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_eye_tracking(filepath)