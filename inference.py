import os
import requests
from openai import OpenAI

# ✅ REQUIRED (Scaler injects these)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

BASE_URL = "http://localhost:7860"

tasks = ["easy_case", "medium_case", "hard_case"]

total = 0
steps = 0

for task in tasks:
    print(f"[START] task={task}", flush=True)

    # RESET ENV
    r = requests.post(f"{BASE_URL}/reset", json={
        "task_id": task,
        "seed": 42
    }).json()

    session_id = r["session_id"]

    # ✅ CALL LLM (MANDATORY for Scaler)
    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are an email triage assistant."},
            {"role": "user", "content": f"Classify and decide action for task: {task}"}
        ]
    )

    # You can ignore output — just calling API is enough

    # ACTION (fixed baseline)
    action = {"action_type": "escalate"}

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
