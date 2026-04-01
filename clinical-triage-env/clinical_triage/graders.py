from .models import Action, Reward
from typing import Dict, Any

class TriageGrader:
    def grade(self, action: Action, case: Dict[str, Any]) -> Reward:
        if action.action_type != "assign_triage_level" or action.triage_level is None:
            return Reward(total=0.0, components={"accuracy": 0.0})
        
        diff = action.triage_level - case["true_triage"]
        
        if diff == 0:
            score = 1.0
        elif abs(diff) == 1:
            score = 0.6
        elif abs(diff) == 2:
            score = 0.2
        else:
            score = 0.0
            
        # Penalty for under-triage
        if diff > 0:
            score -= 0.15
            
        return Reward(total=max(0.0, score), components={"accuracy": score})

class WorkupGrader:
    def grade(self, action: Action, case: Dict[str, Any]) -> Reward:
        if action.action_type != "order_workup" or action.workup_items is None:
            return Reward(total=0.0, components={"sensitivity": 0.0, "specificity": 0.0, "cost_efficiency": 0.0, "safety": 0.0})
            
        required = set(case.get("required_workup", []))
        ordered = set(action.workup_items)
        
        if not required:
            sensitivity = 1.0
        else:
            sensitivity = len(ordered.intersection(required)) / len(required)
            
        if not ordered:
            specificity = 1.0
        else:
            specificity = len(required.intersection(ordered)) / len(ordered)
            
        cost_efficiency = 1.0
        if len(ordered) > 6:
            cost_efficiency -= (len(ordered) - 6) * 0.1
            cost_efficiency = max(0.0, cost_efficiency)
            
        safety = 1.0 # assume safe for now unless explicit contraindications
        
        total = (sensitivity * 0.45) + (specificity * 0.25) + (cost_efficiency * 0.15) + (safety * 0.15)
        
        return Reward(total=total, components={
            "sensitivity": sensitivity, 
            "specificity": specificity, 
            "cost_efficiency": cost_efficiency, 
            "safety": safety
        })

class DispositionGrader:
    def grade(self, action: Action, case: Dict[str, Any]) -> Reward:
        # Evaluate primary diagnosis accuracy and disposition
        primary_diag = action.primary_diagnosis or ""
        true_diag = case.get("true_diagnosis", "")
        
        # Simple fuzzy text match placeholder
        diag_score = 1.0 if true_diag.lower() in primary_diag.lower() or primary_diag.lower() in true_diag.lower() else 0.5
        if not primary_diag:
            diag_score = 0.0
            
        diff_score = 1.0 if action.differential else 0.0
        
        true_disp = case.get("true_disposition", "")
        disp_score = 1.0 if action.disposition == true_disp else 0.0
        
        reasoning_score = 1.0 if action.disposition_reasoning else 0.0
        
        total = (diag_score * 0.35) + (diff_score * 0.25) + (disp_score * 0.30) + (reasoning_score * 0.10)
        
        return Reward(total=total, components={
            "diagnosis_accuracy": diag_score,
            "differential_completeness": diff_score,
            "disposition_accuracy": disp_score,
            "reasoning_quality": reasoning_score
        })
