import os

# List of common filler words to detect
FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "so", "right", "you know"]


def count_filler_words(transcript_text):
    """
    Counts filler word occurrences in a transcript.

    Parameters:
        transcript_text (str): the transcribed speech text

    Returns:
        dict: filler counts, total words, total fillers, rate per 100 words
    """
    transcript_lower = transcript_text.lower()
    words = transcript_lower.split()
    total_words = len(words)

    filler_counts = {}

    for filler in FILLER_WORDS:
        count = 0
        for word in words:
            if word == filler:
                count += 1
        if count > 0:
            filler_counts[filler] = count

    total_fillers = sum(filler_counts.values())

    if total_words > 0:
        filler_rate = round((total_fillers / total_words) * 100, 1)
    else:
        filler_rate = 0.0

    print(f"\n  🗣  Filler Word Stats:")
    print(f"     Total words   : {total_words}")
    print(f"     Total fillers : {total_fillers}")
    print(f"     Filler rate   : {filler_rate} per 100 words")
    if filler_counts:
        print(f"     Breakdown     : {filler_counts}")

    return {
        'filler_counts': filler_counts,
        'total_fillers': total_fillers,
        'total_words': total_words,
        'filler_rate': filler_rate
    }
if __name__ == "__main__":
    transcript_files = [f for f in os.listdir("output") if f.endswith("_transcript.txt")]
    if not transcript_files:
        print("No transcript files found. Run transcriber.py first.")
    else:
        latest = sorted(transcript_files)[-1]
        filepath = os.path.join("output", latest)

        with open(filepath, "r", encoding="utf-8") as f:
            transcript_text = f.read()

        print(f"Testing with: {filepath}")
        results = count_filler_words(transcript_text)