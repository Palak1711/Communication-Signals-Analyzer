import librosa
import librosa.display
import numpy as np
import os

SILENCE_THRESHOLD = 0.02
MIN_SILENCE_DURATION = 0.5
SAMPLE_RATE = 16000

def load_audio(filepath):
    """
    Loads a WAV file into a numpy array.

    Parameters:
        filepath (str): path to the WAV file.

    Returns:
        tuple: (y, sr) where y is audio array, sr is sample rate.
               Returns (None, None) if file not found.
    """
    if not os.path.exists(filepath):
        print(f"  ✗ File not found: {filepath}")
        return None, None

    y, sr = librosa.load(filepath, sr=SAMPLE_RATE, mono=True)
    print(f"  ✓ Audio loaded: {len(y)} samples, {len(y)/sr:.1f} seconds")
    return y, sr

def get_volume_stats(y, sr):
    """
    Calculates average volume, max volume and volume variation.

    Parameters:
        y (np.array): audio data
        sr (int): sample rate

    Returns:
        dict: volume statistics
    """
    # Compute RMS energy for every small frame of audio
    # hop_length=512 means compute RMS every 512 samples
    # At 16000 Hz, 512 samples = 0.032 seconds
    rms = librosa.feature.rms(y=y, hop_length=512)[0]

    avg_volume = float(np.mean(rms))
    max_volume = float(np.max(rms))
    min_volume = float(np.min(rms))
    volume_variation = float(np.std(rms))

    print(f"\n  📊 Volume Stats:")
    print(f"     Average volume : {avg_volume:.4f}")
    print(f"     Max volume     : {max_volume:.4f}")
    print(f"     Variation      : {volume_variation:.4f}")

    return {
        'avg_volume': avg_volume,
        'max_volume': max_volume,
        'min_volume': min_volume,
        'volume_variation': volume_variation
    }


def get_pause_stats(y, sr):
    """
    Detects pauses and calculates speaking vs silence statistics.

    Returns:
        dict: pause statistics including count, duration, speaking percentage
    """
    # Split audio into non-silent intervals
    # top_db=40 means anything 40dB below the max is considered silence
    # This is a standard threshold for indoor speech
    intervals = librosa.effects.split(y, top_db=40)

    total_duration = len(y) / sr

    # Calculate total speaking time from non-silent intervals
    speaking_duration = 0.0
    pause_durations = []

    for i, (start, end) in enumerate(intervals):
        # Each interval is in samples — convert to seconds
        start_sec = start / sr
        end_sec = end / sr
        speaking_duration += (end_sec - start_sec)

        # Detect pauses between consecutive speaking intervals
        if i > 0:
            prev_end = intervals[i-1][1] / sr
            pause_length = start_sec - prev_end
            if pause_length >= MIN_SILENCE_DURATION:
                pause_durations.append(pause_length)

    silence_duration = total_duration - speaking_duration
    speaking_pct = (speaking_duration / total_duration) * 100
    silence_pct = 100 - speaking_pct

    num_pauses = len(pause_durations)
    avg_pause = float(np.mean(pause_durations)) if pause_durations else 0.0
    longest_pause = float(max(pause_durations)) if pause_durations else 0.0

    print(f"\n  ⏸  Pause Stats:")
    print(f"     Speaking    : {speaking_pct:.1f}%")
    print(f"     Silence     : {silence_pct:.1f}%")
    print(f"     Pauses      : {num_pauses}")
    print(f"     Longest     : {longest_pause:.2f}s")
    print(f"     Average     : {avg_pause:.2f}s")

    return {
        'total_duration': total_duration,
        'speaking_duration': speaking_duration,
        'silence_duration': silence_duration,
        'speaking_percentage': speaking_pct,
        'silence_percentage': silence_pct,
        'num_pauses': num_pauses,
        'avg_pause_duration': avg_pause,
        'longest_pause': longest_pause,
        'pause_durations': pause_durations
    }

def analyze_audio(filepath):
    """
    Master function — runs all audio analysis on a WAV file.

    Parameters:
        filepath (str): path to WAV file from audio_recorder.py

    Returns:
        dict: complete audio analysis results, or None if file not found
    """
    print(f"\n{'='*45}")
    print(f"  Analyzing audio: {filepath}")
    print(f"{'='*45}")

    # Step 1: Load the audio file
    y, sr = load_audio(filepath)
    if y is None:
        return None

    # Step 2: Get volume statistics
    volume_stats = get_volume_stats(y, sr)

    # Step 3: Get pause statistics
    pause_stats = get_pause_stats(y, sr)

    # Step 4: Combine everything into one result dictionary
    results = {
        'filepath': filepath,
        **volume_stats,
        **pause_stats
    }

    print(f"\n  ✓ Audio analysis complete.")
    return results


# Test block — runs only when executing this file directly
if __name__ == "__main__":
    import os
    # Find the most recent WAV file in output/
    wav_files = [f for f in os.listdir("output") if f.endswith(".wav")]
    if not wav_files:
        print("No WAV files found in output/. Run audio_recorder.py first.")
    else:
        latest = sorted(wav_files)[-1]
        filepath = os.path.join("output", latest)
        print(f"Testing with: {filepath}")
        results = analyze_audio(filepath)
        if results:
            print(f"\n{'='*45}")
            print("  FINAL RESULTS")
            print(f"{'='*45}")
            for key, value in results.items():
                if key != 'pause_durations':
                    print(f"  {key}: {value}")


