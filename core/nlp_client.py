import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    print("  ✗ No GEMINI_API_KEY found. Add it to your .env file.")
    client = None
else:
    client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3-flash-preview"


def test_api_connection():
    """Sends a minimal test message to confirm the API key works."""
    if client is None:
        print("  ✗ Cannot test — no API client available.")
        return None

    print("\n  🔌 Testing Gemini API connection...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with exactly: API connection successful.",
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant."
            )
        )
        reply = response.text
        print(f"  ✓ API responded: {reply}")
        return reply

    except Exception as e:
        print(f"  ✗ API call failed: {e}")
        return None


if __name__ == "__main__":
    test_api_connection()