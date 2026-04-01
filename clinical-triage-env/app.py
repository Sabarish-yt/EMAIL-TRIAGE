print("🚀 Email Triage App Starting...")

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from clinical_triage import ClinicalTriageEnv, Action

app = FastAPI(title="Email Triage OpenEnv")

sessions = {}

class ResetRequest(BaseModel):
    task_id: str
    seed: int = 42

class StepRequest(BaseModel):
    session_id: str
    action: Action

@app.post("/reset")
def reset_env(req: ResetRequest):
    try:
        env = ClinicalTriageEnv(task_id=req.task_id, seed=req.seed)
        obs = env.reset()
        session_id = str(uuid.uuid4())
        sessions[session_id] = env
        return {"session_id": session_id, "observation": obs.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/state/{session_id}")
def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id].state()


@app.post("/step")
def step_env(req: StepRequest):
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    env = sessions[req.session_id]
    obs, reward, done, info = env.step(req.action)
    
    if done:
        del sessions[req.session_id]
        
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    }

import gradio as gr

def run_env():
    return """
    # ✅ Clinical Triage OpenEnv Running
    
    ### Available Endpoints:
    - /reset
    - /step
    - /state
    
    👉 Go to /docs for API testing
    """

demo = gr.Interface(
    fn=run_env,
    inputs=[],
    outputs="markdown"
)

# ❌ REMOVE THIS
# demo.launch()

# ✅ ADD THIS
app = gr.mount_gradio_app(app, demo, path="/")
