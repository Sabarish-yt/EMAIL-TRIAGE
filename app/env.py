from typing import Tuple, Dict, Any
from app.models import Observation, Action, Reward
from app.data import EMAIL_DATA
from app.graders import grade_action

class EmailTriageEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.reset()

    def reset(self) -> Observation:
        self.emails = EMAIL_DATA[self.task].copy()
        self.index = 0
        self.total_reward = 0
        self.done = False
        return self.state()

    def state(self) -> Observation:
        current = None
        if self.index < len(self.emails):
            current = self.emails[self.index]

        return Observation(
            inbox=self.emails,
            current_email=current,
            step_count=self.index
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:
        if self.done:
            return self.state(), 0.0, True, {}

        email = self.emails[self.index]
        reward, info = grade_action(self.task, email, action)

        self.total_reward += reward
        self.index += 1

        if self.index >= len(self.emails):
            self.done = True

        return self.state(), reward, self.done, info
