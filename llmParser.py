import google.generativeai as genai
import config

def check_name(text):
    prompt = "This text is a physical therapy note, return 1 if there is a human name detected, return 0 otherwise. Text is as follows: " + text
    response = model.generate_content(prompt).text.split()[0]

    if (response == '1'):
        return True
    elif (response == '0'):
        return False
    else:
        print("Error in parsing the LLM response to either 1 or 0")
        return False

def check_soap_note_llm(text):
    return check_name(text)

soap_note_text = open("output_text.txt", "r").read()
genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
print(check_soap_note_llm(soap_note_text))