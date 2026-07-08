import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils


def analyze_face_detection(video_filepath):
    """
    Processes a video file frame by frame, detecting face landmarks
    using MediaPipe Face Mesh. Saves one sample annotated frame
    and reports the detection rate across the whole video.

    Parameters:
        video_filepath (str): path to the AVI video file

    Returns:
        dict: total_frames, frames_with_face, detection_rate
    """
    if not os.path.exists(video_filepath):
        print(f"  ✗ Video not found: {video_filepath}")
        return None
    print(f"\n  👀 Analyzing face detection: {video_filepath}")

    cap = cv2.VideoCapture(video_filepath)

    total_frames = 0
    frames_with_face = 0
    saved_sample = False
    sample_path = "output/face_sample.jpg"

    with mp_face_mesh.FaceMesh(static_image_mode=False) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            total_frames += 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks is not None:
                frames_with_face += 1

                if not saved_sample:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION
                        )
                    cv2.imwrite(sample_path, frame)
                    saved_sample = True

    cap.release()

    if total_frames > 0:
        detection_rate = round((frames_with_face / total_frames) * 100, 1)
    else:
        detection_rate = 0.0

    print(f"  ✓ Total frames        : {total_frames}")
    print(f"  ✓ Frames with face    : {frames_with_face}")
    print(f"  ✓ Detection rate      : {detection_rate}%")
    if saved_sample:
        print(f"  ✓ Sample saved to     : {sample_path}")

    return {
        'total_frames': total_frames,
        'frames_with_face': frames_with_face,
        'detection_rate': detection_rate
    }


if __name__ == "__main__":
    avi_files = [f for f in os.listdir("output") if f.endswith(".avi")]
    if not avi_files:
        print("No video files found. Run video_recorder.py first.")
    else:
        latest = sorted(avi_files)[-1]
        filepath = os.path.join("output", latest)
        results = analyze_face_detection(filepath)