import google.generativeai as genai
import config
import re
import sys

def check_name(text):
    prompt = "This text is a physical therapy note, return 1 if there is a human name detected right before the DOB, return 0 otherwise. Text is as follows: " + text
    response = model.generate_content(prompt).text.split()[0]

    if (response == '1'):
        print("A name is detected, autofail pass!")
        return True
    elif (response == '0'):
        return False
    else:
        print(response)
        print("Error in parsing the LLM response to either 1 or 0")
        return False

def check_rubric(text):
    total_pts = 0

    chat = model.start_chat(
    history=[
        {"role": "user", "parts": "This text is extracted from a physical therapy note, help me assess it against multiple rubric items. Here's the text: " + text},
        {"role": "model", "parts": "I got the text, what are the rubric items and how do I respond?"},
        {"role": "user", "parts": "Each rubric item has multiple subitems and corresponding points. The grading scale is: full points for Correctly Documented, half points for Errors in Documentation, and no point for Not documented. Assess the text based on the subitems, and give them points based on the grading scale. Add up the points to get the final points for the entire rubric item. Make sure that your final output should be in this format: full final points, brief reason. For example: '2, name is not included'"},
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
        if point < config.THRESHOLD * 4:
            print("Demographic section points fell below threshold.")
            print("Assessment: Unskilled")
            sys.exit(0)
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        print(f"Reason for deduction: {reason}")
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
        if point < config.THRESHOLD * 10:
            print("Demographic section points fell below threshold.")
            print("Assessment: Unskilled")
            sys.exit(0)
        reason = split_parts[1].strip()  # Remove leading/trailing spaces
        total_pts += int(point)
        print(f"Reason for deduction: {reason}")
    else:
        print("Error processing History section.")

    print("Completed rubric checking.")

    if (float(total_pts)/14 < config.THRESHOLD): return False
    return True

def check_soap_note_llm(text):
    return check_name(text) and check_rubric(text)
    
soap_note_text = open("output_text.txt", "r").read()
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
result = check_soap_note_llm(soap_note_text)
print("Assessment: ", "Skilled" if result else "Unskilled")