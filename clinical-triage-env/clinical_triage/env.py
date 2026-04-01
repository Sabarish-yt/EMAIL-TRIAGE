from typing import Tuple, Dict, Any, Optional
import random
from .models import Observation, Action, Reward
from .cases import CASES
from .graders import TriageGrader, WorkupGrader, DispositionGrader

class ClinicalTriageEnv:
    def __init__(self, task_id: str, seed: int = 42):
        self.task_id = task_id
        self.seed = seed
        self.rng = random.Random(seed)
        self.current_step = 0
        self.case = None
        self.obs = None
        
        if task_id == "easy_case":
            self.max_steps = 3
            self.grader = TriageGrader()
            self.instructions = "Assign an ESI triage level (1-5) based on vitals and chief complaint."
        elif task_id == "medium_case":
            self.max_steps = 5
            self.grader = WorkupGrader()
            self.instructions = "Order appropriate diagnostic workup."
        elif task_id == "hard_case":
            self.max_steps = 5
            self.grader = DispositionGrader()
            self.instructions = "Set primary diagnosis, differential, and recommend disposition."
        else:
            raise ValueError(f"Unknown task_id: {task_id}")

    def reset(self) -> Observation:
        self.current_step = 0
        case_matches = [c for c in CASES if c["id"] == self.task_id]
        self.case = case_matches[0] if case_matches else self.rng.choice(CASES)
        
        self.obs = Observation(
            patient_id=self.case["id"],
            age=self.case["age"],
            sex=self.case["sex"],
            chief_complaint=self.case["chief_complaint"],
            arrival_mode=self.case["arrival_mode"],
            vitals=self.case["vitals"],
            history=self.case["history"],
            ros=self.case["ros"],
            physical_exam=self.case["physical_exam"],
            labs_ordered=[],
            labs_resulted=[],
            imaging_ordered=[],
            imaging_resulted=[],
            consults_ordered=[],
            triage_level_assigned=None,
            step_number=self.current_step,
            task_id=self.task_id,
            instructions=self.instructions
        )
        return self.obs

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.current_step += 1
        self.obs.step_number = self.current_step
        
        done = False
        info = {}
        
        # Check if the right action was taken for the task
        if self.task_id == "easy_case" and action.action_type == "assign_triage_level":
            done = True
            reward = self.grader.grade(action, self.case)
            self.obs.triage_level_assigned = action.triage_level
        elif self.task_id == "medium_case" and action.action_type == "order_workup":
            done = True
            reward = self.grader.grade(action, self.case)
        elif self.task_id == "hard_case" and action.action_type == "recommend_disposition":
            done = True
            reward = self.grader.grade(action, self.case)
        else:
            # Intermediate step or invalid
            done = self.current_step >= self.max_steps
            reward = self.grader.grade(action, self.case) if done else Reward(total=0.0, components={})
            if not done and reward.total > 0:
                reward.total *= 0.3 # Intermediate penalty/scale
                
        return self.obs, reward, done, info

    def state(self) -> Dict[str, Any]:
        if self.obs is None:
            return {}
        return self.obs.model_dump()
