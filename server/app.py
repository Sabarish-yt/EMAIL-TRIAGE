print("📧 Email Triage OpenEnv Starting...")

from fastapi import FastAPI, HTTPException, Request
from typing import Dict, Any
import uuid

app = FastAPI(title="Email Triage OpenEnv")

# ==============================
# ENVIRONMENT
# ==============================

class EmailTriageEnv:
    def __init__(self, task_id="easy_case", seed=42):
        self.task_id = task_id
        self.seed = seed
        self.step_count = 0
        self.done = False

    def reset(self):
        self.step_count = 0
        self.done = False

        return {
            "email": {
                "subject": "Refund request",
                "body": "I want my money back",
                "sender": "user@example.com"
            },
            "step_count": self.step_count
        }

    def step(self, action: Dict[str, Any]):
        self.step_count += 1

        # Reward logic
        if self.task_id == "easy_case":
            reward_value = 1.0
        elif self.task_id == "medium_case":
            reward_value = 0.7
        elif self.task_id == "hard_case":
            reward_value = 0.9
        else:
            reward_value = 0.0

        self.done = True

        return (
            {"result": "processed"},   # observation
            {"total": reward_value},   # ✅ reward MUST be dict
            self.done,
            {}
        )

    def state(self):
        return {
            "task_id": self.task_id,
            "step_count": self.step_count,
            "done": self.done
        }

# ==============================
# SESSION STORAGE
# ==============================

sessions: Dict[str, EmailTriageEnv] = {}

# ==============================
# RESET (SCALAR SAFE)
# ==============================

@app.post("/reset")
async def reset_env(request: Request):
    try:
        # Handle empty body safely
        try:
            data = await request.json()
        except:
            data = {}

        task_id = data.get("task_id", "easy_case")
        seed = data.get("seed", 42)

        env = EmailTriageEnv(task_id=task_id, seed=seed)
        obs = env.reset()

        session_id = str(uuid.uuid4())
        sessions[session_id] = env

        return {
            "session_id": session_id,
            "observation": obs
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==============================
# STEP (VALIDATION FIXED)
# ==============================

@app.post("/step")
async def step_env(request: Request):
    try:
        data = await request.json()

        session_id = data.get("session_id")
        action = data.get("action", {})

        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        env = sessions[session_id]
        obs, reward, done, info = env.step(action)

        if done:
            del sessions[session_id]

        return {
            "observation": obs,
            "reward": {
                "total": reward.get("total", 0.0)
            },
            "done": done,
            "info": info
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==============================
# STATE
# ==============================

@app.get("/state/{session_id}")
def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return sessions[session_id].state()

# ==============================
# ROOT (OPTIONAL)
# ==============================

@app.get("/")
def home():
    return {"message": "Email Triage OpenEnv is running"}
