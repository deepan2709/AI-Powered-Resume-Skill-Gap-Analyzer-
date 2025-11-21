# src/matching.py

def compare_skills(candidate_skills, role_skills):
    """
    Compare the candidate's skills with role requirements and return:
    - matched skills
    - missing skills
    - score percentage
    """
    # Convert both lists to lowercase sets
    candidate_set = set([s.lower().strip() for s in candidate_skills])
    role_set = set([s.lower().strip() for s in role_skills])

    # Intersection (matched)
    matched = sorted(candidate_set & role_set)
    # Difference (missing)
    missing = sorted(role_set - candidate_set)

    # Fit score
    total = len(role_set)
    score = round((len(matched) / total * 100), 1) if total > 0 else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "score": score
    }
