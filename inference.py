import requests

BASE_URL = "https://sabaxr-sabarihv3.hf.space"

def run():
    tasks = ["easy_case", "medium_case", "hard_case"]
    total = 0

    for t in tasks:
        # RESET
        r = requests.post(f"{BASE_URL}/reset", json={
            "task_id": t,
            "seed": 42
        }).json()

        sid = r["session_id"]

        # ACTION
        action = {"action_type": "escalate"}

        # STEP
        res = requests.post(f"{BASE_URL}/step", json={
            "session_id": sid,
            "action": action
        }).json()

        total += res["reward"]["total"]

    print("Final Score:", total)

if __name__ == "__main__":
    run()
