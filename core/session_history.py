import os
import json

HISTORY_FILE = "session_history.json"  # project root, NOT inside output/


def load_history():
    """
    Loads past session scores. Returns an empty list if no
    history exists yet (first-ever real session).
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_session_to_history(session_timestamp, final_results):
    """
    Appends this session's TRUE scores to history. Only called
    for real sessions where speech was actually detected — silent
    or invalid takes never reach this function at all.
    """
    history = load_history()

    entry = {
        'timestamp': session_timestamp,
        'final_score': final_results['final_score'],
        'voice_score': final_results['voice_score'],
        'body_score': final_results['body_score'],
        'comm_score': final_results['comm_score'],
        'needs_retry': final_results['needs_retry']
    }
    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"  ✓ Session saved to history ({len(history)} total sessions)")
    return history


def show_progress(history):
    """Prints a simple first-session-to-latest-session comparison."""
    if len(history) < 2:
        print("  (Need at least 2 sessions to show progress)")
        return

    first_score = history[0]['final_score']
    latest_score = history[-1]['final_score']
    change = round(latest_score - first_score, 1)

    sign = "+" if change >= 0 else ""
    print(f"\n  📈 Progress: {first_score} -> {latest_score} "
          f"({sign}{change} over {len(history)} sessions)")