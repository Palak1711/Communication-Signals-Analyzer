def eye_contact_to_score(pct):
    """Converts eye contact percentage into a 0-100 score."""
    if pct < 30:
        return 20
    elif pct < 50:
        return 50
    elif pct < 70:
        return 80
    elif pct < 85:
        return 100
    else:
        return 85


def head_stability_to_score(moves_per_second):
    """Converts head movement rate into a 0-100 score. Lower is better."""
    if moves_per_second < 0.5:
        return 95
    elif moves_per_second < 1.0:
        return 85
    elif moves_per_second < 1.5:
        return 70
    elif moves_per_second < 2.5:
        return 50
    else:
        return 25


def blink_rate_to_score(blinks_per_minute):
    """
    Converts blink rate into a 0-100 score. Unlike other converters,
    this one peaks in the MIDDLE of the range - both too low and
    too high score worse than a comfortable natural rate.
    """
    if blinks_per_minute < 8:
        return 60
    elif blinks_per_minute < 15:
        return 85
    elif blinks_per_minute < 25:
        return 95
    elif blinks_per_minute < 35:
        return 60
    else:
        return 30


def calculate_body_language_score(eye_contact_results, head_movement_results,
                                    expression_results, blink_results):
    """
    Combines eye contact, head stability, facial expressiveness, and
    blink rate into one weighted Body Language Score.

    Weights (matching the original research-based plan):
        Eye contact:      50%
        Head stability:   25%
        Expressiveness:   15%
        Blink rate:       10%
    """
    eye_score = eye_contact_to_score(eye_contact_results['eye_contact_percentage'])
    head_score = head_stability_to_score(head_movement_results['movements_per_second'])
    expr_score = expression_results['expression_score']  # already 0-100
    blink_score = blink_rate_to_score(blink_results['blinks_per_minute'])

    body_language_score = (
        (eye_score * 0.50) +
        (head_score * 0.25) +
        (expr_score * 0.15) +
        (blink_score * 0.10)
    )
    body_language_score = round(body_language_score, 1)

    print(f"\n  🧍 Body Language Score: {body_language_score}/100")
    print(f"     Eye contact    : score {eye_score}")
    print(f"     Head stability : score {head_score}")
    print(f"     Expressiveness : score {expr_score}")
    print(f"     Blink rate     : score {blink_score}")

    return {
        'body_language_score': body_language_score,
        'eye_score': eye_score,
        'head_score': head_score,
        'expr_score': expr_score,
        'blink_score': blink_score
    }