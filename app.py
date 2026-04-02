print("📧 Email Triage OpenEnv Starting...")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid

app = FastAPI(title="Email Triage OpenEnv")

# ==============================
# Simple Environment Logic
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

        # simple scoring logic
        reward = 0.0

        if self.task_id == "easy_case":
            reward = 1.0
        elif self.task_id == "medium_case":
            reward = 0.7
        elif self.task_id == "hard_case":
            reward = 0.9

        self.done = True

        return (
            {"result": "processed"},
            {"total": reward},
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
# Request Models
# ==============================

class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy_case"
    seed: Optional[int] = 42

class StepRequest(BaseModel):
    session_id: str
    action: Dict[str, Any]

# ==============================
# Session Storage
# ==============================

sessions: Dict[str, EmailTriageEnv] = {}

# ==============================
# API Endpoints (SCALAR FIXED)
# ==============================

@app.post("/reset")
def reset_env(req: Optional[ResetRequest] = None):
    try:
        # ✅ SCALAR FIX: allow empty body
        task_id = "easy_case"
        seed = 42

        if req:
            task_id = req.task_id
            seed = req.seed

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


@app.post("/step")
def step_env(req: StepRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    env = sessions[req.session_id]
    obs, reward, done, info = env.step(req.action)

    if done:
        del sessions[req.session_id]

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state/{session_id}")
def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return sessions[session_id].state()
