
# Responsibility: record audio from microphone, save as WAV file
# Used by: main.py

import sounddevice as sd    
import soundfile as sf      
import numpy as np           
import os                   
from datetime import datetime  

# Settings — written in UPPERCASE because these don't change
SAMPLE_RATE = 16000  
CHANNELS = 1          
OUTPUT_DIR = "output" 

def record_audio(duration=10, filename_timestamp=None):
    """
    Records audio from the default microphone and saves it as a WAV file.

    Parameters:
        duration (int): how many seconds to record. Default is 10.

    Returns:
        str: filepath of the saved WAV file.
    """

    # Create output/ folder if it doesn't exist yet
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build a unique filename using current date and time
    # Example result: session_20260626_143022.wav
    if filename_timestamp is None:
      filename_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # os.path.join() builds file paths in an OS-independent way (Windows uses '\' while Linux/macOS use '/')
    filename = f"session_{filename_timestamp}.wav"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Tell the user recording is starting
    print("\n=========================================")
    print(f"  Recording for {duration} seconds...")
    print("  Speak now — just talk naturally.")
    print("=========================================")

    # Start recording
    # duration * SAMPLE_RATE = total samples to collect
    # e.g. 10 seconds x 16000 = 160,000 samples
    audio_data = sd.rec(
        frames=int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    )

    # Show a live countdown while recording runs in background
    import time
    for remaining in range(duration, 0, -1):
        print(f"\r  ⏱  {remaining} seconds remaining...", end="", flush=True)
        time.sleep(1)

    # Wait until recording is fully finished before saving
    sd.wait()

    print("\n  ✓ Recording complete!")

    # Save the numpy array as a WAV file
    sf.write(filepath, audio_data, SAMPLE_RATE)
    print(f"  ✓ Saved to: {filepath}")

    ## Return the filepath so it can be used by the next stage of the pipeline.
    return filepath

# This only runs when you execute this file directly
# It does NOT run when main.py imports this file
if __name__ == "__main__":
    print("Testing audio recorder...")
    saved_path = record_audio(duration=5)
    print(f"\nTest complete. File saved at: {saved_path}")
    print("Go to output/ folder and play the WAV file to verify.")