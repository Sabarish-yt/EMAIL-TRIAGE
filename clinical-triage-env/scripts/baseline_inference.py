import argparse
import json
import os
import requests

def run_baseline(task, seed, verbose):
    url_base = "http://localhost:8000"
    
    print(f"Running baseline for {task} with seed {seed}")
    
    try:
        resp = requests.post(f"{url_base}/reset", json={"task_id": task, "seed": seed})
        resp.raise_for_status()
        data = resp.json()
        session_id = data["session_id"]
        obs = data["observation"]
        
        if verbose:
            print("Initial Observation:", json.dumps(obs, indent=2))
            
        action = None
        if task == "easy_vitals_triage":
            # Simple heuristic
            action = {"action_type": "assign_triage_level", "triage_level": 1 if obs["vitals"]["hr"] > 100 else 4}
        elif task == "medium_workup_ordering":
            action = {"action_type": "order_workup", "workup_items": ["ECG", "CT_CHEST", "TROPONIN", "CBC", "BMP", "COAGS"]}
        elif task == "hard_differential_disposition":
            action = {
                "action_type": "set_diagnosis",
                "primary_diagnosis": "Acute Myocardial Infarction",
                "differential": ["AMI", "PE", "Pneumonia"],
                "confidence": 0.9
            }
            resp = requests.post(f"{url_base}/step", json={"session_id": session_id, "action": action})
            action = {
                "action_type": "recommend_disposition",
                "disposition": "admit_icu",
                "disposition_reasoning": "Elevated HR, abnormal vitals."
            }
            
        resp = requests.post(f"{url_base}/step", json={"session_id": session_id, "action": action})
        resp.raise_for_status()
        res = resp.json()
        
        if verbose:
            print("Reward:", json.dumps(res["reward"], indent=2))
            
        return res["reward"]["total"]
    except Exception as e:
        print(f"Error running inference: {e}")
        return 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--task", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()
    
    tasks = [args.task] if args.task else ["easy_vitals_triage", "medium_workup_ordering", "hard_differential_disposition"]
    
    results = {}
    for t in tasks:
        results[t] = run_baseline(t, args.seed, args.verbose)
        
    print("Baseline Results:", results)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
