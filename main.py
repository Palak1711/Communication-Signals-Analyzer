# main.py
# Entry point for Communication Signal Analyzer
# Today: records audio AND video simultaneously using threads
# Then analyzes the recorded audio for communication signals


import threading
from datetime import datetime
from core.audio_recorder import record_audio
from core.video_recorder import record_video
from core.audio_analyzer import analyze_audio


def show_header(): 
    print("=" * 45)
    print("  Communication Signal Analyzer v0.1")
    print("=" * 45)

def run_session(duration=10):
    """
    Runs one full recording session.
    Audio and video are recorded simultaneously using threads.
    Analyze the recorded audio file     
    Display communication signals
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
    # This is the moment both recording start at the same time
    audio_thread.start()
    video_thread.start()

    # Wait for BOTH threads to finish before continuing
    # .join() means "wait here until this thread is done"
    # We wait for audio first, then video
    # The program won't move past these two lines until both are done
    audio_thread.join()
    video_thread.join()


    # After recording finishes, analyze the saved WAV file

    print("\n" + "=" * 45)
    print("  Recording complete! Now analyzing...")
    print("=" * 45)


    # Pass recorded audio path to analyzer
    if results.get('audio'):

        audio_results = analyze_audio(results['audio'])

        
        # Display extracted communication signals
        if audio_results:

            print("\n  Communication Signals:")
            print(f"  Speaking   : {audio_results['speaking_percentage']:.1f}%")
            print(f"  Pauses     : {audio_results['num_pauses']}")
            print(f"  Avg Volume : {audio_results['avg_volume']:.4f}")
            print(f"  Variation  : {audio_results['volume_variation']:.4f}")


    # Both recordings are now complete
    print("\n" + "=" * 45)
    print("  Session complete!")
    print(f"  Audio: {results.get('audio', 'Failed')}")
    print(f"  Video: {results.get('video', 'Failed')}")
    print("=" * 45)

if __name__ == "__main__":
    run_session(duration=10)