import google.generativeai as genai
import config

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
        {"role": "user", "parts": "Each rubric item has multiple subitems and corresponding points. The grading scale is: full points for Correctly Documented, half points for Errors in Documentation, and no point for Not documented. Assess the text based on the subitems, and give them points based on the grading scale. Add up the points to get the final points for the entire rubric item. Your final output should be in this format: final integer points, brief reason. For example: '2, name is not included'"},
        {"role": "model", "parts": "Got it! Now show me the rubric items one by one, and I will return the point as an integer for each item."},
        ]
    )
    # DEMOGRAPHICS (4 points)
    response = chat.send_message("Rubric item: demographics, 4 points in total. 2 points for complete patient identification (Age, Birthdate, Gender, Employment), and 2 points for complete referral mechanism.")
    print(response.text)
    # total_pts += int(response.text)
    # print(response.text + " points for DEMOGRAPHICS")

    # HISTORY (10 points)
    response = chat.send_message("Rubric item: history, 10 points in total. - Past Medical and Surgical history: 1 point" +  
        "- Social history/Home set-up (e.g., Alcohol and Tobacco use, cultural concerns, hobbies): 1 point  " +  
        "- Current condition/Chief complaint/Onset of symptoms/Mechanism of injury: 2 points  " +  
        "- Prior functional status/Activity level/Behaviors: 1 point  " +  
        "- Medications/Allergies: 1 point  " +  
        "- Diagnostic Imaging/Pertinent lab values: 1 point  " +  
        "- History of falls: 1 point  " +  
        "- Patient’s goals for therapy: 2 points ")
    # print(response.text)
    # total_pts += int(response.text)
    # print(response.text + " points for HISTORY")

    # other items can follow similar format
    # response = chat.send_message("")
    # print(int(response.text))

    print("check rubric completed")

    # dummy threshold
    if (total_pts < 60): return False
    return True

def check_soap_note_llm(text):
    # check_rubric(text)
    return check_name(text) and check_rubric(text)

soap_note_text = open("output_text.txt", "r").read()
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
print(check_soap_note_llm(soap_note_text))