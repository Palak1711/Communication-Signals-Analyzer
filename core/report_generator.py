import os


def generate_report(session_timestamp, final_results, communication_results):
    """
    Builds a formatted text report. If the session scored below
    the low-score threshold, the report leads with encouragement
    and focus areas instead of the raw number.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("  COMMUNICATION SIGNALS ANALYZER — SESSION REPORT")
    lines.append("=" * 50)
    lines.append(f"Session: {session_timestamp}")
    if communication_results and communication_results.get('low_confidence'):
        lines.append("⚠ Note: Transcription confidence was low this session — AI feedback may be less reliable.")
    lines.append("")

    if final_results['needs_retry']:
        lines.append("This session could use another take before scoring feels meaningful.")
        lines.append("Here's what to focus on for your next try:")
        lines.append("")
    else:
        lines.append(f"OVERALL SCORE: {final_results['final_score']}/100")
        lines.append("")
        lines.append("Breakdown:")
        lines.append(f"  Voice Score          : {final_results['voice_score']}/100")
        lines.append(f"  Body Language Score  : {final_results['body_score']}/100")
        lines.append(f"  Communication Score  : {final_results['comm_score']}/100")
        lines.append("")

    if communication_results:
        strengths_label = "What's working:" if final_results['needs_retry'] else "Strengths:"
        lines.append(strengths_label)
        for s in communication_results.get('strengths', []):
            lines.append(f"  + {s}")
        lines.append("")

        weak_label = "Focus on these for your next try:" if final_results['needs_retry'] else "Areas to improve:"
        lines.append(weak_label)
        for w in communication_results.get('weaknesses', []):
            lines.append(f"  - {w}")
        lines.append("")

        lines.append("Example improvement:")
        lines.append(f"  Original: \"{communication_results.get('weak_sentence_original','')}\"")
        lines.append(f"  Improved: \"{communication_results.get('weak_sentence_improved','')}\"")
        lines.append(f"  Why: {communication_results.get('improvement_explanation','')}")

    report_text = "\n".join(lines)

    report_path = os.path.join("output", f"session_{session_timestamp}_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n  📄 Full report saved to: {report_path}")
    return report_path