from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: str
    subject: str
    body: str
    sender: str

class Observation(BaseModel):
    inbox: List[Email]
    current_email: Optional[Email]
    step_count: int

class Action(BaseModel):
    action_type: str  # "classify", "reply", "escalate", "ignore"
    label: Optional[str] = None
    response: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str
