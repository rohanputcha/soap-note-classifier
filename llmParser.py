import google.generativeai as genai
import config
import re
import sys

def check_name(text):
    prompt = "This text is a physical therapy note, return 1 if there is a human name detected only right top above DOB in the title, ignore any name in the main content, return 0 otherwise. Text is as follows: " + text
    response = model.generate_content(prompt).text.split()[0]
    print(response)

    if (response == '1'):
        print("A name is detected, autofail pass!")
        print("-" * 100)
        return True
    elif (response == '0'):
        print("A name is not detected, autofail fails!")
        print("-" * 100)
        return False
    else:
        print(response)
        print("Error in parsing the LLM response to either 1 or 0")
        return False

def check_rubric(text):
    total_pts = 0
    unskilled_sections = []

    chat = model.start_chat(
    history=[
        {"role": "user", "parts": "This text is extracted from a physical therapy note, help me assess it against multiple rubric items. Here's the text: " + text},
        {"role": "model", "parts": "I got the text, what are the rubric items and how do I respond?"},
        {"role": "user", "parts": "Each rubric item has multiple subitems and corresponding points. The grading scale is: full points for Correctly Documented, half points for Errors in Documentation, and no point for Not documented. Assess the text based on the subitems, and give them points based on the grading scale. Add up the points to get the final points for the entire rubric item. Make sure that your final output should be in this format: full final points, brief reason. For example: '2, name is not included'. Please only call out obvious flaws -- be otherwise lenient."},
        {"role": "model", "parts": "Got it! Now show me the rubric items one by one, and I will return the point as an integer for each item."},
        ]
    )
    
    response = chat.send_message("Rubric item: demographics, 4 points in total. 2 points for complete patient identification (Age, Birthdate, Gender, Employment), and 2 points for complete referral mechanism. Return the number of points earned, with a maximum of 4, followed by a comma to delimit.")

    # DEMOGRAPHICS (4 points)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Demographic section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 4:
            print("Demographic section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Demographics")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 4:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Demographic section.")


    # HISTORY (10 points)
    response = chat.send_message("Rubric item: history, 10 points in total. - Past Medical and Surgical history: 1 point" +  
        "- Social history/Home set-up (e.g., Alcohol and Tobacco use, cultural concerns, hobbies): 1 point  " +  
        "- Current condition/Chief complaint/Onset of symptoms/Mechanism of injury: 2 points  " +  
        "- Prior functional status/Activity level/Behaviors: 1 point  " +  
        "- Medications/Allergies: 1 point  " +  
        "- Diagnostic Imaging/Pertinent lab values: 1 point  " +  
        "- History of falls: 1 point  " +  
        "- Patient’s goals for therapy: 2 points. Return the number of points earned, with a maximum of 10, followed by a comma to delimit.")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"History section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("History section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("History")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 10:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing History section.")

    
    # SYSTEMS REVIEW (10 points)
    response = chat.send_message("Rubric item: system review, 10 points in total." +
        "- Cardiopulmonary: Vitals, Edema: 2 points" + 
        "- Integumentary: Color, Integrity: 2 points" +
        "- Musculoskeletal: Gross ROM, Strength, Posture, Height, Weight, BMI: 2 points" +
        "- Neuromuscular: Gross mobility, Gross movement, Gross sensation: 2 points" +
        "- Communication: Ability, Affect, Cognition, Language, Learning style: 2 points")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"System Review section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("System Review section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("System Review")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 10:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing System Review section.")


    # EVALUATION and PT DIAGNOSIS (10 points)
    response = chat.send_message("Rubric item: Evaluation and PT Diagnosis, 10 points in total." +
        "- Impairments: 2 points" + 
        "- Activity limitations: 2 points" + 
        "- Movement System Diagnoses and/or Cardiopulmonary Diagnosis: 2 points" + 
        "- ICD-10 codes: 2 points")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Evaluation and PT Diagnosis section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Evaluation and PT Diagnosis section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Evaluation and PT Diagnosis")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 10:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Evaluation and PT Diagnosis section.")

    
    # PROGNOSIS (10 points)
    response = chat.send_message("Rubric item: Prognosis, 10 points in total." +
        "- Functional outcome expectations and timeframe: 5 points" + 
        "- Key factors impacting outcomes: 2 points" + 
        "- Risks, precautions, and/or safety concerns: 3 points")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Prognosis section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Prognosis section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Prognosis")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 10:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Prognosis section.")

    # GOALS (12 points)
    response = chat.send_message("Rubric item: Goals, 12 points in total." +
        "- Specific: 3 points" +
        "- Measurable: 3 points" +
        "- Achievable: 2 points" +
        "- Relevant: 2 points" +
        "- Time-bound: 2 points")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Goals section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Goals section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Goals")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 12:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Goals section.")

    
    # PLAN OF CARE (15 points)
    response = chat.send_message("Rubric item: Plan of Care, 15 points in total." +
        "- Specific interventions to be used: 5 points" +
        "- Patient/caregiver education: 2 points" +
        "- Delegation: 2 points" +
        "- Proposed duration: 2 points" +
        "- Proposed frequency: 2 points" +
        "- Anticipated transition of care plans: 2 points")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Plan of Care section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Plan of Care section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Plan of Care")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 15:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Plan of Care section.")

    
    # AUTHENTICATION and BILLING (9 points)
    response = chat.send_message("Rubric item: Authentication and Billing, 9 points in total." +
        "- Signature: 1 point" +
        "- Title: 1 point" +
        "- Treatment provided today: 2 points" +
        "- Charges (CPT codes) for today: 1 point" +
        "- G-Codes and modifiers (if applicable): 1 point" +
        "- Spelling/proper use of abbreviations: 2 points" +
        "- Date/time: 1 point")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Authentication and Billing section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Authentication and Billing section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Authentication and Billing")
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 9:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Authentication and Billing section.")

    
    # TEST AND MEASURES (20 points)
    response = chat.send_message("Rubric item: Test and Measures, 20 points. For each performed outcome measure only, assess how good it is documented. The total point is 20. Measure list: " +
        "- Aerobic Capacity; - Anthropometric Characteristics; - Assistive Technology; " +
        "- Balance; - Circulation; - Community, Social, and Civic Life; - Cranial and Peripheral Nerve Integrity; " +
        "- Education; - Life Environmental Factors; - Gait (Quality, assistance, devices, distance); " +
        "- Integumentary Integrity; - Joint Integrity and Mobility; - Mental Functions; " +
        "- Mobility (Including Locomotion); - Motor Function; - Muscle Performance; Neuromotor Development and Sensory; " +
        "- Processing; - Pain (Intensity, location, pattern, descriptions, and aggravating or relieving factors); " +
        "- Posture; - Range of Motion; - Reflex Integrity; - Self-Care and Domestic Life; " +
        "- Sensory Integrity; - Skeletal Integrity; - Special tests")
    # print(response.text)
    split_parts = re.split(r", |\. ", response.text, maxsplit=1)
    if len(split_parts) == 2:
        # Check if the point is a fraction
        point_str = split_parts[0].strip()
        if "/" in point_str:  # Handle fractional points
            numerator, denominator = map(int, point_str.split("/"))
            point = numerator
        else:
            point = int(point_str)  # Handle whole numbers
            
        print(f"Test and Measures section points: {point}")
        print("-" * 50)
        if point < config.THRESHOLD * 10:
            print("Test and Measures section points fell below threshold.")
            print("Assessment: Unskilled")
            # sys.exit(0)
            unskilled_sections.append("Test and Measures")
        reason = split_parts[1].strip().replace('*', '')  # Remove leading/trailing spaces
        total_pts += int(point)
        if point < 20:
            print(f"Reason for deduction: {reason}")
        print("-" * 100)
    else:
        print("Error processing Test and Measures section.")


    print("Completed rubric checking. Total points: " + str(total_pts))

    if (float(total_pts)/100 < config.THRESHOLD or unskilled_sections): return unskilled_sections
    return None

def check_soap_note_llm(text):
    name = check_name(text)
    if not name:
        print("Final Assessment: Unskilled")
        sys.exit(0)
    rubric = check_rubric(text)
    return name and rubric
    
soap_note_text = open("output_text.txt", "r").read()
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
result = check_soap_note_llm(soap_note_text)

if result:
    print("Unskilled sections: ")
    for section in result:
        print('  > ' + section)
    print("Final Assessment: Unskilled")
    print("-" * 100)
else:
    print("Final Assessment: Skilled")
    print("-" * 100)