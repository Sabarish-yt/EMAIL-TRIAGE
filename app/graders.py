def grade_action(task, email, action):
    score = 0.0
    reason = ""

    if "refund" in email.subject.lower():
        if action.action_type == "classify" and action.label == "billing":
            score += 0.4
        if action.action_type == "reply":
            score += 0.6

    elif "fraud" in email.subject.lower():
        if action.action_type == "escalate":
            score = 1.0

    elif "angry" in email.subject.lower():
        if action.action_type == "reply":
            if "sorry" in (action.response or "").lower():
                score = 1.0

    # Penalize useless actions
    if action.action_type == "ignore":
        score -= 0.2

    return max(0.0, min(score, 1.0)), {"reason": reason}
