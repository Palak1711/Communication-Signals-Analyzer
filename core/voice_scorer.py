def wpm_to_score(wpm):
    """Converts words-per-minute into a 0-100 score."""
    if wpm < 100:
        return 20
    elif wpm < 130:
        return 50
    elif wpm < 170:
        return 95
    elif wpm < 200:
        return 70
    else:
        return 50


def speaking_pct_to_score(pct):
    """Converts speaking percentage into a 0-100 score."""
    if pct < 50:
        return 30
    elif pct < 70:
        return 65
    elif pct < 85:
        return 95
    else:
        return 75
    
def filler_rate_to_score(rate):
    """Converts filler rate (per 100 words) into a 0-100 score."""
    if rate < 2:
        return 100
    elif rate < 5:
        return 80
    elif rate < 10:
        return 55
    elif rate < 15:
        return 30
    else:
        return 10


def volume_variation_to_score(variation):
    """Converts volume variation into a 0-100 score."""
    if variation < 0.01:
        return 30
    elif variation < 0.02:
        return 60
    elif variation < 0.04:
        return 90
    else:
        return 75

def calculate_voice_score(audio_stats, filler_stats):
    """
    Combines audio and filler statistics into one Voice Score.

    Parameters:
        audio_stats (dict): output from analyze_audio() in Day 4
        filler_stats (dict): output from count_filler_words() in Day 6

    Returns:
        dict: voice_score and the breakdown of each component
    """
    total_words = filler_stats['total_words']
    duration = audio_stats['total_duration']

    if duration > 0:
        wpm = (total_words / duration) * 60
    else:
        wpm = 0

    wpm_score = wpm_to_score(wpm)
    speaking_score = speaking_pct_to_score(audio_stats['speaking_percentage'])
    filler_score = filler_rate_to_score(filler_stats['filler_rate'])
    variation_score = volume_variation_to_score(audio_stats['volume_variation'])

    voice_score = (
        (wpm_score * 0.25) +
        (speaking_score * 0.25) +
        (filler_score * 0.25) +
        (variation_score * 0.25)
    )
    voice_score = round(voice_score, 1)

    print(f"\n  🎯 Voice Score: {voice_score}/100")
    print(f"     WPM            : {round(wpm,1)} -> score {wpm_score}")
    print(f"     Speaking %     : score {speaking_score}")
    print(f"     Filler rate    : score {filler_score}")
    print(f"     Voice variation: score {variation_score}")

    return {
        'voice_score': voice_score,
        'wpm': round(wpm, 1),
        'wpm_score': wpm_score,
        'speaking_score': speaking_score,
        'filler_score': filler_score,
        'variation_score': variation_score
    }