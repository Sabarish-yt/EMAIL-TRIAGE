from clinical_triage import ClinicalTriageEnv, Action

def test_easy_vitals_triage():
    env = ClinicalTriageEnv(task_id="easy_vitals_triage", seed=42)
    obs = env.reset()
    assert obs.chief_complaint is not None
    
    action = Action(action_type="assign_triage_level", triage_level=1)
    obs, reward, done, info = env.step(action)
    
    assert done is True
    assert reward.total >= 0.0

def test_medium_workup_ordering():
    env = ClinicalTriageEnv(task_id="medium_workup_ordering", seed=42)
    env.reset()
    
    action = Action(
        action_type="order_workup",
        workup_items=["CT_CHEST", "ECG"]
    )
    obs, reward, done, info = env.step(action)
    
    assert done is True

def test_hard_differential_disposition():
    env = ClinicalTriageEnv(task_id="hard_differential_disposition", seed=42)
    env.reset()
    
    env.step(Action(
        action_type="set_diagnosis",
        primary_diagnosis="Acute decompensated heart failure",
        differential=["ADHF", "COPD exacerbation"],
        confidence=0.85,
    ))
    
    obs, reward, done, info = env.step(Action(
        action_type="recommend_disposition",
        disposition="admit_icu",
        disposition_reasoning="High severity"
    ))
    assert done is True
