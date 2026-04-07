import requests

BASE_URL = "http://localhost:7860"

tasks = ["easy_case", "medium_case", "hard_case"]

total = 0
steps = 0

for task in tasks:
    print(f"[START] task={task}", flush=True)

    # RESET
    r = requests.post(f"{BASE_URL}/reset", json={
        "task_id": task,
        "seed": 42
    }).json()

    session_id = r["session_id"]

    # ACTION
    action = {"action_type": "escalate"}

    # STEP
    res = requests.post(f"{BASE_URL}/step", json={
        "session_id": session_id,
        "action": action
    }).json()

    reward = res["reward"]["total"]
    total += reward
    steps += 1

    print(f"[STEP] task={task} step=1 reward={reward}", flush=True)

    print(f"[END] task={task} score={reward} steps=1", flush=True)

print(f"Final Score: {total}", flush=True)
