
📧 Email Triage OpenEnv

An AI-powered email triage environment built using FastAPI and OpenEnv principles.
This project simulates real-world email classification and response decision-making tasks.

🚀 Features
✅ OpenEnv-compatible environment (reset, step, state)
✅ 3 difficulty levels:
Easy → Spam detection
Medium → Account issue handling
Hard → Legal complaint escalation
✅ Reward-based evaluation system
✅ FastAPI backend + Gradio UI
✅ Baseline agent implementation
✅ Dockerized deployment
📊 Tasks
Task	Description	Expected Action
easy_case	Spam email	ignore
medium_case	Account hacked request	escalate
hard_case	Legal complaint threat	escalate
🎯 Reward System

All rewards are strictly within (0, 1):

Task	Correct Action	Reward
easy_case	ignore	0.95
medium_case	escalate	0.75
hard_case	escalate	0.85
🛠️ API Endpoints
🔹 Reset Environment
POST /reset

Request:

{
  "task_id": "easy_case",
  "seed": 42
}
🔹 Step
POST /step

Request:

{
  "session_id": "xxx",
  "action": {
    "action_type": "escalate"
  }
}
🔹 State
GET /state/{session_id}
🧪 Running Locally
pip install -r requirements.txt
python -m server.app

Open in browser:

http://localhost:7860
🐳 Docker
docker build -t email-triage .
docker run -p 7860:7860 email-triage
🤖 Inference

Run:

python inference.py

✔ Uses LiteLLM proxy via:

API_BASE_URL
API_KEY

✔ Prints structured logs:

[START]
[STEP]
[END]
📁 Project Structure
repo/
├── server/
│   └── app.py
├── inference.py
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
✅ Submission Notes
✔ OpenEnv compliant
✔ Multi-mode deployment ready
✔ Uses Scaler-provided API proxy
✔ Structured logging enabled
✔ Rewards strictly within (0,1)
🎉 Final Output

The system evaluates tasks and produces a final score based on agent decisions.

👨‍💻 Author

Sabarish S
