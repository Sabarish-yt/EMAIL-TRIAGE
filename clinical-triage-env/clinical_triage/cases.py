from .models import Vitals, PatientHistory, ReviewOfSystems

CASES = [
    {
        "id": "easy_case",
        "age": 58,
        "sex": "M",
        "chief_complaint": "Chest pain, 10/10 severity, radiating to left arm, diaphoresis",
        "arrival_mode": "EMS",
        "vitals": Vitals(hr=110, bp="90/60", rr=24, temp=37.1, spo2=92, pain=10, gcs=15, weight_kg=85.0),
        "history": PatientHistory(pmh=["Hypertension", "Hyperlipidemia", "Type 2 Diabetes"], medications=["Metformin", "Lisinopril", "Atorvastatin"], allergies=["Penicillin"], social_hx="Smoker (1 pack/day for 30 years)"),
        "ros": ReviewOfSystems(positive=["Chest pain", "Diaphoresis", "Shortness of breath", "Nausea"], negative=["Fever", "Cough", "Abdominal pain", "Leg swelling", "Headache"]),
        "physical_exam": {
            "General": "Diaphoretic, clutching chest, appears to be in severe distress.",
            "Cardiovascular": "Tachycardic, regular rhythm, no murmurs, rubs, or gallops.",
            "Respiratory": "Clear to auscultation bilaterally, tachypneic.",
            "Abdomen": "Soft, non-tender, non-distended.",
            "Neurological": "Alert and oriented x3, no focal deficits."
        },
        "true_triage": 1,
        "required_workup": ["ECG", "TROPONIN", "CT_CHEST", "CBC", "BMP", "COAGS", "CARDIOLOGY_CONSULT"],
        "true_diagnosis": "Acute Myocardial Infarction",
        "true_disposition": "admit_icu"
    },
    {
        "id": "medium_case",
        "age": 22,
        "sex": "F",
        "chief_complaint": "Twisted right ankle while playing soccer",
        "arrival_mode": "walk-in",
        "vitals": Vitals(hr=80, bp="110/70", rr=14, temp=36.8, spo2=99, pain=6, gcs=15, weight_kg=62.0),
        "history": PatientHistory(pmh=[], medications=[], allergies=[], social_hx="None"),
        "ros": ReviewOfSystems(positive=["Right ankle pain"], negative=["Fever", "Other injuries"]),
        "physical_exam": {
            "General": "Alert, no acute distress.",
            "Extremities": "Swelling and tenderness over right lateral malleolus, able to bear weight for 4 steps."
        },
        "true_triage": 4,
        "required_workup": ["XRAY_EXTREMITY"],
        "true_diagnosis": "Ankle sprain",
        "true_disposition": "discharge"
    },
    {
        "id": "hard_case",
        "age": 72,
        "sex": "M",
        "chief_complaint": "Productive cough, fever, confusion",
        "arrival_mode": "EMS",
        "vitals": Vitals(hr=115, bp="100/60", rr=28, temp=39.2, spo2=90, pain=2, gcs=13, weight_kg=70.0),
        "history": PatientHistory(pmh=["COPD", "CHF"], medications=["Albuterol", "Furosemide"], allergies=["Sulfa"], social_hx="Ex-smoker"),
        "ros": ReviewOfSystems(positive=["Cough", "Fever", "Confusion", "Dyspnea"], negative=["Chest pain", "Abdominal pain"]),
        "physical_exam": {
            "General": "Acutely ill appearing, confused.",
            "Respiratory": "Decreased breath sounds right lower lobe with crackles.",
            "Neurological": "Confused, not oriented to time or place."
        },
        "true_triage": 2,
        "required_workup": ["CXR", "CBC", "CMP", "BLOOD_CULTURE", "LACTATE", "ABG"],
        "true_diagnosis": "Sepsis secondary to pneumonia",
        "true_disposition": "admit_icu"
    }
]
