LOW_SCORE_THRESHOLD = 40


def calculate_final_score(voice_score_results, body_language_results, communication_results):
    """
    Combines Voice, Body Language, and Communication scores into
    one overall Communication Signals Score.

    Weights: Voice 40%, Body Language 30%, Communication 30%
    Floor rule: if any single pillar is severely weak (<30),
    the overall score is capped at 60.

    Low-score handling: if the final score falls below
    LOW_SCORE_THRESHOLD, the raw number is not shown as the
    headline — the session is framed as "try again" with
    specific focus areas instead of a discouraging number.
    The true score is still calculated and returned for
    internal use (e.g. session history).
    """
    voice_score = voice_score_results['voice_score']
    body_score = body_language_results['body_language_score']

    if communication_results:
        comm_score = communication_results['communication_score']
    else:
        comm_score = 50.0  # neutral fallback if AI analysis failed

    final_score = (
        (voice_score * 0.40) +
        (body_score * 0.30) +
        (comm_score * 0.30)
    )
    final_score = round(final_score, 1)

    weakest_pillar = min(voice_score, body_score, comm_score)
    floor_applied = False
    if weakest_pillar < 30 and final_score > 60:
        final_score = 60.0
        floor_applied = True

    needs_retry = final_score < LOW_SCORE_THRESHOLD

    if needs_retry:
        print(f"\n  🔁 This session needs a bit more practice before scoring feels meaningful.")
        print(f"     No score shown this time — check the report for what to focus on.")
    else:
        print(f"\n  🏆 Communication Signals Score: {final_score}/100")
        print(f"     Voice Score        : {voice_score}")
        print(f"     Body Language Score: {body_score}")
        print(f"     Communication Score: {comm_score}")
        if floor_applied:
            print(f"     ⚠  Floor rule applied — one pillar was severely weak")

    return {
        'final_score': final_score,
        'voice_score': voice_score,
        'body_score': body_score,
        'comm_score': comm_score,
        'floor_applied': floor_applied,
        'needs_retry': needs_retry
    }