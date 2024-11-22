# Define the rubric as a dictionary
rubric = {
    "DEMOGRAPHICS": [
        {"item": "Patient identification (Age, Birthdate, Gender, Employment)", "points": 2},
        {"item": "Referral mechanism", "points": 2}
    ],
    "HISTORY": [
        {"item": "Past Medical and Surgical history", "points": 1},
        {"item": "Social history/Home set-up (e.g., Alcohol and Tobacco use, cultural concerns, hobbies)", "points": 1},
        {"item": "Current condition/Chief complaint/Onset of symptoms/Mechanism of injury", "points": 2},
        {"item": "Prior functional status/Activity level/Behaviors", "points": 1},
        {"item": "Medications/Allergies", "points": 1},
        {"item": "Diagnostic Imaging/Pertinent lab values", "points": 1},
        {"item": "History of falls", "points": 1},
        {"item": "Patient’s goals for therapy", "points": 2}
    ],
    "SYSTEMS REVIEW": [
        {"item": "Cardiopulmonary: Vitals, Edema", "points": 2},
        {"item": "Integumentary: Color, Integrity", "points": 2},
        {"item": "Musculoskeletal: Gross ROM, Strength, Posture, Height, Weight, BMI", "points": 2},
        {"item": "Neuromuscular: Gross mobility, Gross movement, Gross sensation", "points": 2},
        {"item": "Communication: Ability, Affect, Cognition, Language, Learning style", "points": 2}
    ],
    "EVALUATION and PT DIAGNOSIS": [
        {"item": "Impairments", "points": 2},
        {"item": "Activity limitations", "points": 2},
        {"item": "Movement System Diagnoses and/or Cardiopulmonary Diagnosis", "points": 4},
        {"item": "ICD-10 codes", "points": 2}
    ],
    "PROGNOSIS": [
        {"item": "Functional outcome expectations and timeframe", "points": 5},
        {"item": "Key factors impacting outcomes", "points": 2},
        {"item": "Risks, precautions, and/or safety concerns", "points": 3}
    ],
    "GOALS": [
        {"item": "Specific", "points": 3},
        {"item": "Measurable", "points": 3},
        {"item": "Achievable", "points": 2},
        {"item": "Relevant", "points": 2},
        {"item": "Time-bound", "points": 2}
    ],
    "PLAN OF CARE": [
        {"item": "Specific interventions to be used", "points": 5},
        {"item": "Patient/caregiver education", "points": 2},
        {"item": "Delegation", "points": 2},
        {"item": "Proposed duration", "points": 2},
        {"item": "Proposed frequency", "points": 2},
        {"item": "Anticipated transition of care plans", "points": 2}
    ],
    "AUTHENTICATION and BILLING": [
        {"item": "Signature", "points": 1},
        {"item": "Title", "points": 1},
        {"item": "Treatment provided today", "points": 2},
        {"item": "Charges (CPT codes) for today", "points": 1},
        {"item": "G-Codes and modifiers (if applicable)", "points": 1},
        {"item": "Spelling/proper use of abbreviations", "points": 2},
        {"item": "Date/time", "points": 1}
    ]
}



# Initialize the total points
total_pts = 0

# Iterate through each section and item
for section, items in rubric.items():
    for item in items:
        prompt = f"Rubric item: {section}, {item['points']} points - {item['item']}"
        # Assuming chat.send_message simulates the AI response
        response = chat.send_message(prompt)
        points_awarded = int(response.text)  # Convert the AI response to an integer
        total_pts += points_awarded
        print(f"{response.text} points awarded for {item['item']}")

# Print the total score
print(f"Total Points: {total_pts}/100")
