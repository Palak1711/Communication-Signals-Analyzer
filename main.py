# main.py
# Entry point for Communication Signal Analyzer
# Records audio AND video simultaneously using threads
# Then analyzes both for communication signals


import threading
from datetime import datetime
from core.audio_recorder import record_audio
from core.video_recorder import record_video
from core.audio_analyzer import analyze_audio
from core.transcriber import transcribe_audio, save_transcript
from core.filler_detector import count_filler_words
from core.voice_scorer import calculate_voice_score
from core.face_analyzer import analyze_face_detection
from core.eye_contact import analyze_eye_contact
from core.head_movement import analyze_head_movement
from core.expression_analyzer import analyze_facial_expression


def show_header():
    print("=" * 45)
    print("  Communication Signal Analyzer v0.1")
    print("=" * 45)

def run_session(duration=10):
    """
    Runs one full recording session.
    Audio and video are recorded simultaneously using threads.
    Analyzes both, then displays communication signals.
    """
    show_header()

    # Generate ONE shared timestamp for this session
    # Both audio and video files will use this same timestamp
    # So session_20260626_143022.wav matches session_20260626_143022.avi
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n  Session ID: {timestamp}")
    print(f"  Duration: {duration} seconds")
    print("\n  Get ready — recording starts now...\n")

    # Store results from both threads here
    # Threads can't return values directly — we use a dictionary
    # to collect results from both threads after they finish
    results = {}

    # Define what the audio thread will do
    def audio_thread_job():
        results['audio'] = record_audio(
            duration=duration,
            filename_timestamp=timestamp
        )

    # Define what the video thread will do
    def video_thread_job():
        results['video'] = record_video(
            duration=duration,
            filename_timestamp=timestamp
        )

    # Create two thread objects
    # target= tells each thread which function to run
    audio_thread = threading.Thread(target=audio_thread_job)
    video_thread = threading.Thread(target=video_thread_job)

    # Start both threads — they now run simultaneously
    # This is the moment both recordings start at the same time
    audio_thread.start()
    video_thread.start()

    # Wait for BOTH threads to finish before continuing
    # .join() means "wait here until this thread is done"
    # The program won't move past these two lines until both are done
    audio_thread.join()
    video_thread.join()

    print("\n" + "=" * 45)
    print("  Recording complete! Now analyzing...")
    print("=" * 45)

    # ============================================
    # AUDIO ANALYSIS BRANCH — everything audio-related
    # ============================================
    if results.get('audio'):

        audio_results = analyze_audio(results['audio'])

        # Display extracted communication signals
        if audio_results:
            print("\n  Communication Signals:")
            print(f"  Speaking   : {audio_results['speaking_percentage']:.1f}%")
            print(f"  Pauses     : {audio_results['num_pauses']}")
            print(f"  Avg Volume : {audio_results['avg_volume']:.4f}")
            print(f"  Variation  : {audio_results['volume_variation']:.4f}")

        transcript_result = transcribe_audio(results['audio'])
        if transcript_result:
            save_transcript(transcript_result['text'], results['audio'])
            filler_results = count_filler_words(transcript_result['text'])
            voice_score_results = calculate_voice_score(audio_results, filler_results)

    
    if results.get('video'):

        face_results = analyze_face_detection(results['video'])
        eye_contact_results = analyze_eye_contact(results['video'])
        head_movement_results = analyze_head_movement(results['video'])
        expression_results = analyze_facial_expression(results['video'])

        if eye_contact_results:
            print("\n  Body Language Signals:")
            print(f"  Eye Contact : {eye_contact_results['eye_contact_percentage']}%")

    # Both recordings are now complete
    print("\n" + "=" * 45)
    print("  Session complete!")
    print(f"  Audio: {results.get('audio', 'Failed')}")
    print(f"  Video: {results.get('video', 'Failed')}")
    print("=" * 45)

if __name__ == "__main__":
    run_session(duration=10)