import json
import os
from core.nlp_client import client, MODEL_NAME
from google.genai import types

SYSTEM_PROMPT = """You are an expert communication coach analyzing a short spoken transcript.

Respond with ONLY valid JSON, no markdown formatting, no code fences, no extra text.
Use exactly this structure:

{
  "structure_score": ,
  "clarity_score": ,
  "vocabulary_score": ,
  "strengths": ["", "", ""],
  "weaknesses": ["", "", ""],
  "weak_sentence_original": "",
  "weak_sentence_improved": "",
  "improvement_explanation": ""
}

Base every field strictly on the transcript provided. If the transcript is
very short or empty, note that honestly in the weaknesses instead of
inventing feedback that isn't grounded in what was actually said."""


def analyze_communication(transcript_text):
    """
    Sends a transcript to Gemini for structured communication feedback.
    Returns None if analysis fails.
    """
    if client is None:
        print("  ✗ Cannot analyze — no API client available.")
        return None

    if not transcript_text or not transcript_text.strip():
        print("  ✗ Empty transcript — skipping communication analysis.")
        return None

    print("\n  🧠 Analyzing communication structure...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"Transcript:\n\n{transcript_text}",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )
        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json", "", 1).strip()

        data = json.loads(raw_text)

        communication_score = round(
            ((data['structure_score'] + data['clarity_score'] + data['vocabulary_score']) / 30) * 100,
            1
        )
        data['communication_score'] = communication_score

        print(f"  ✓ Communication Score: {communication_score}/100")
        print(f"     Structure  : {data['structure_score']}/10")
        print(f"     Clarity    : {data['clarity_score']}/10")
        print(f"     Vocabulary : {data['vocabulary_score']}/10")

        return data

    except json.JSONDecodeError as e:
        print(f"  ✗ Could not parse AI response as JSON: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Communication analysis failed: {e}")
        return None


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
        results = analyze_communication(transcript_text)