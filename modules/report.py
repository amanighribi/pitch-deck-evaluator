def generate_report(evaluation: dict) -> dict:
    overall = evaluation["overall_score"]

    if overall >= 80:
        verdict = "Strong Opportunity"
        color = "green"
    elif overall >= 60:
        verdict = "Worth Further Diligence"
        color = "orange"
    elif overall >= 40:
        verdict = "Needs Significant Work"
        color = "orange"
    else:
        verdict = "Not Investment Ready"
        color = "red"

    return {
        "overall_score": overall,
        "verdict": verdict,
        "color": color,
        "recommendation": evaluation["recommendation"],
        "investment_readiness": evaluation["investment_readiness"],
        "readiness_detail": evaluation["readiness_detail"],
        "communication": evaluation["communication"],
        "narrative": evaluation["narrative"],
        "problem_solution_fit": evaluation["problem_solution_fit"],
        "slide_coverage": evaluation["slide_coverage"],
        "missing_investor_signals": evaluation["missing_investor_signals"],
        "top_risks": evaluation["top_risks"],
        "investor_questions": evaluation["investor_questions"],
    }