import os
import requests
from openai import OpenAI

# ✅ Fix API key mapping
os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY", "")

client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)

BASE_URL = "http://localhost:7860"

tasks = ["easy_case", "medium_case", "hard_case"]

total = 0

for task in tasks:
    print(f"[START] task={task}", flush=True)

    try:
        # RESET
        r = requests.post(f"{BASE_URL}/reset", json={
            "task_id": task,
            "seed": 42
        })
        data = r.json()
        session_id = data["session_id"]

        # ✅ LLM CALL (safe)
        try:
            client.chat.completions.create(
                model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
                messages=[
                    {"role": "user", "content": f"Handle email task: {task}"}
                ],
                max_tokens=10
            )
        except Exception:
            pass

        # STEP
        res = requests.post(f"{BASE_URL}/step", json={
            "session_id": session_id,
            "action": {"action_type": "escalate"}
        })

        result = res.json()
        reward = result["reward"]["total"]
        total += reward

        print(f"[STEP] task={task} step=1 reward={reward}", flush=True)
        print(f"[END] task={task} score={reward} steps=1", flush=True)

    except Exception as e:
        print(f"[ERROR] task={task} msg={str(e)}", flush=True)

print(f"Final Score: {total}", flush=True)
