# main.py
# Entry point for Communication Signal Analyzer
# Orchestrates the full pipeline — today just recording

from core.audio_recorder import record_audio

def show_header():
    print("=" * 45)
    print("  Communication Signal Analyzer v0.1")
    print("=" * 45)

def run_session(duration=10):
    """Runs one full analysis session."""
    show_header()

    # Step 1: Record audio
    audio_file = record_audio(duration=duration)

    # Step 2 onwards: coming in future days
    print("\n[Recording done — analysis coming in future days]")
    print(f"Audio saved at: {audio_file}")

if __name__ == "__main__":
    run_session(duration=10)