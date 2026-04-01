from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

ActionType = Literal[
    "assign_triage_level", 
    "order_workup", 
    "set_diagnosis", 
    "recommend_disposition", 
    "request_info"
]

class Action(BaseModel):
    action_type: ActionType
    
    # For assign_triage_level
    triage_level: Optional[int] = None           # 1 (most critical) to 5 (non-urgent)
    
    # For order_workup
    workup_items: Optional[List[str]] = None     # See full catalog below
    
    # For set_diagnosis
    primary_diagnosis: Optional[str] = None      # Free-text diagnosis string
    differential: Optional[List[str]] = None     # Ranked list of diagnoses
    confidence: Optional[float] = None           # 0.0-1.0
    
    # For recommend_disposition
    disposition: Optional[str] = None            # discharge | observation | admit_floor | admit_icu | transfer
    disposition_reasoning: Optional[str] = None  # Free-text clinical justification
    
    # For request_info
    info_requested: Optional[str] = None         # Clarifying question (informational only)

class Vitals(BaseModel):
    hr: int
    bp: str
    rr: int
    temp: float
    spo2: int
    pain: int
    gcs: int
    weight_kg: float

class PatientHistory(BaseModel):
    pmh: List[str]
    medications: List[str]
    allergies: List[str]
    social_hx: str

class ReviewOfSystems(BaseModel):
    positive: List[str]
    negative: List[str]

class WorkupItem(BaseModel):
    name: str
    status: Literal["ordered", "resulted"]

class LabResult(BaseModel):
    name: str
    value: str
    abnormal: bool

class ImagingResult(BaseModel):
    name: str
    finding: str

class Observation(BaseModel):
    patient_id: str
    age: int
    sex: str                        # M / F / Other
    chief_complaint: str
    arrival_mode: str               # walk-in / EMS / transfer
    vitals: Vitals                  # HR, BP, RR, Temp, SpO2, Pain, GCS, Weight
    history: PatientHistory         # PMH, medications, allergies, social hx
    ros: ReviewOfSystems            # Positive/negative system findings
    physical_exam: Dict[str, str]   # System -> exam finding
    labs_ordered: List[WorkupItem]
    labs_resulted: List[LabResult]
    imaging_ordered: List[WorkupItem]
    imaging_resulted: List[ImagingResult]
    consults_ordered: List[WorkupItem]
    triage_level_assigned: Optional[int] = None
    step_number: int
    task_id: str
    instructions: str               # Task-specific instructions for the agent

class Reward(BaseModel):
    total: float
    components: Dict[str, float]
