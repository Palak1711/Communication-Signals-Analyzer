import threading
from datetime import datetime
from core.audio_recorder import record_audio
from core.video_recorder import record_video
from core.audio_analyzer import analyze_audio
from core.transcriber import transcribe_audio, save_transcript
from core.filler_detector import count_filler_words
from core.voice_scorer import calculate_voice_score
from core.eye_contact import analyze_eye_contact
from core.head_movement import analyze_head_movement
from core.expression_analyzer import analyze_facial_expression
from core.blink_detector import analyze_blink_rate
from core.body_language_scorer import calculate_body_language_score
from core.communication_analyzer import analyze_communication
from core.final_scorer import calculate_final_score
from core.report_generator import generate_report
from core.session_history import save_session_to_history


def run_web_session(duration=10):
    """
    Runs one full recording + analysis session for the web interface.
    Same pipeline as main.py's run_session(), but returns a result
    dictionary instead of printing, and skips the interactive
    "press Enter" pause since a button click already means ready.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}

    def audio_thread_job():
        results['audio'] = record_audio(duration=duration, filename_timestamp=timestamp)

    def video_thread_job():
        results['video'] = record_video(duration=duration, filename_timestamp=timestamp)

    audio_thread = threading.Thread(target=audio_thread_job)
    video_thread = threading.Thread(target=video_thread_job)
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()

    audio_results = None
    voice_score_results = None
    communication_results = None
    body_language_results = None

    if results.get('audio'):
        audio_results = analyze_audio(results['audio'])
        transcript_result = transcribe_audio(results['audio'])
        if transcript_result:
            save_transcript(transcript_result['text'], results['audio'])
            filler_results = count_filler_words(transcript_result['text'])
            voice_score_results = calculate_voice_score(audio_results, filler_results)
            communication_results = analyze_communication(transcript_result['text'])

    if results.get('video'):
        try:
            eye_contact_results = analyze_eye_contact(results['video'])
            head_movement_results = analyze_head_movement(results['video'])
            expression_results = analyze_facial_expression(results['video'])
            blink_results = analyze_blink_rate(results['video'])
            body_language_results = calculate_body_language_score(
                eye_contact_results, head_movement_results,
                expression_results, blink_results
            )
        except Exception:
            body_language_results = None

    if not voice_score_results or not body_language_results:
        return {'status': 'error', 'message': 'Analysis could not be completed.'}

    if audio_results['speaking_percentage'] < 5:
        return {'status': 'no_speech'}

    final_results = calculate_final_score(voice_score_results, body_language_results, communication_results)
    if not final_results:
        return {'status': 'error', 'message': 'Could not calculate a final score.'}

    generate_report(timestamp, final_results, communication_results)
    save_session_to_history(timestamp, final_results)

    return {
        'status': 'ok',
        'final_score': final_results['final_score'],
        'needs_retry': final_results['needs_retry'],
        'voice_score': final_results['voice_score'],
        'body_score': final_results['body_score'],
        'comm_score': final_results['comm_score'],
        'strengths': communication_results.get('strengths', []) if communication_results else [],
        'weaknesses': communication_results.get('weaknesses', []) if communication_results else []
    }