import whisper
import os

print("  Loading Whisper model (this happens once, may take a moment)...")
model = whisper.load_model("base")
print("  ✓ Whisper model loaded.")


def transcribe_audio(filepath):
    """
    Converts a WAV audio file into text using Whisper.

    Parameters:
        filepath (str): path to the WAV file to transcribe.

    Returns:
        dict: {'text': full transcript, 'segments': list of timed segments}
              Returns None if transcription fails.
    """
    if not os.path.exists(filepath):
        print(f"  ✗ File not found: {filepath}")
        return None
    
    print(f"\n  🎙  Transcribing: {filepath}")
    print("  This may take a few seconds...")

    try:
        result = model.transcribe(filepath, fp16=False)
    except Exception as e:
        print(f"  ✗ Transcription failed: {e}")
        return None

    transcript_text = result['text'].strip()
    segments = result['segments']

    print(f"  ✓ Transcription complete.")
    print(f"\n  Transcript:")
    print(f"  \"{transcript_text}\"")

    return {
        'text': transcript_text,
        'segments': segments
    }

def save_transcript(transcript_text, audio_filepath):
    """
    Saves the transcript text to a .txt file matching the audio filename.
    """
    base_name = os.path.splitext(audio_filepath)[0]
    transcript_path = base_name + "_transcript.txt"

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print(f"  ✓ Transcript saved to: {transcript_path}")
    return transcript_path


if __name__ == "__main__":
    wav_files = [f for f in os.listdir("output") if f.endswith(".wav")]
    if not wav_files:
        print("No WAV files found. Run audio_recorder.py first.")
    else:
        latest = sorted(wav_files)[-1]
        filepath = os.path.join("output", latest)

        result = transcribe_audio(filepath)
        if result:
            save_transcript(result['text'], filepath)