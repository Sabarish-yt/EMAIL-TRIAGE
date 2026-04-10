📧 Email Triage OpenEnv
This project simulates a real-world email triage system...

📧 Email Triage OpenEnv
An interactive, reinforcement learning OpenEnv designed to simulate a real-world customer support workflow where autonomous (or rule-based) agents process incoming emails, triage issues, and escalate urgent problems.

Email Triage AI OpenEnv FastAPI

📌 Project Overview
This environment evaluates the ability of AI agents to intelligently categorize and respond to customer emails ranging from simple requests to high-priority legal threats and fraud alerts.

Spaces & Components
Action Space:
classify: Group the email with a label.
reply: Directly reply to the customer with an appropriate response.
escalate: Immediately escalate the email (e.g. for potential fraud).
ignore: Discard spam and unimportant emails.
Observation Space:
The agent receives an observation with the current active email (subject, body, sender), the remaining inbox, and current step_count.
Reward Engine:
A deterministic grader assigns continuous partial rewards based on classification accuracy, penalizes ignoring important threads (-0.2), and awards maximum reward (1.0) for perfect responses to angry complaints and necessary escalations for fraud.
🚀 The Tasks
Easy: Simple classification and billing inquiries (e.g., Refund requests, login issues).
Medium: Identifying high-priority escalations (e.g., Fraud alerts, feature requests).
Hard: Emotional intelligence and de-escalation (e.g., Angry complaints, legal threats).
📊 Baseline Performance
Baseline Score: 2.6 / 3.0 using rule-based agent

The baseline uses rule-based heuristics to approximate classification, while the environment supports LLM-based agents for improved performance.

💻 Quick Start & Deployment
1. Docker Deployment (Recommended)
You can directly build and run the baseline agent via Docker:

docker build -t email-env .
docker run email-env
(You should see an output of Final Score: 2.6 or similar.)

2. Local Python Environment
Ensure you are in the project folder and have your environment set up:

pip install -r requirements.txt
python -m baseline.run_baseline
🌟 Bonus functionality: Web UI!
To gain deeper intuition on how to step through this environment, you can run the interactive UI dashboard:

uvicorn app.ui:app --reload
Then navigate to http://localhost:8000 in your browser!

👨‍💻 Author

Sabarish S
