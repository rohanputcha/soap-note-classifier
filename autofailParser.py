import re
import config
import sys

def extract_objective_section(text):
    """
    Extract all text from the Objective section up to the Assessment section,
    or from Exercises/Activities up to the next SOAP section.
    """
    objective_match = re.search(r'(Objective|Exercises/Activities)\s*[:\-]?\s*(.*?)(?=(Subjective|Assessment|Plan|$))', text, re.IGNORECASE | re.DOTALL)
    if objective_match:
        return objective_match.group(2).strip()
    return ""

def extract_time(text):
    """
    Extract all time entries (in minutes) from the text.
    """
    time_matches = re.findall(r'(\d+)\s*min(?:ute)?(?:s)?', text, re.IGNORECASE)
    total_time = sum(int(match) for match in time_matches)
    return total_time

def check_medicare_8_minute_rule(text):
    """
    Check if the total time in the Objective section exceeds 8 minutes.
    """
    objective_text = extract_objective_section(text)
    total_time = extract_time(objective_text)
    if total_time < 8:
        return False  # Reject if total time is less than 8 minutes
    return True

def check_incorrect_billing(text):
    """
    Check for common billing codes and ensure they seem logical within the Objective section.
    """
    objective_text = extract_objective_section(text)
    billing_matches = re.findall(r'(CPT\s*code|units|billing|charged)', objective_text, re.IGNORECASE)
    
    if not billing_matches:
        return False  # If no billing information is provided in the Objective section, it's an issue.

    # Further validation logic could go here; for now, we assume if billing exists, it's valid.
    return True

def check_treatment_frequency_and_duration(text):
    frequency_patterns = [
        r'\d+\s*x\s*/?\s*week',                 
        r'\d+\s*times?\s*/?\s*(per|a)?\s*week', 
        r'once\s*(per)?\s*week',                
        r'weekly'                                
    ]
    
    duration_patterns = [
        r'for\s+\d+\s*week(?:s)?',            
        r'for\s+\d+\s*month(?:s)?',          
        r'over\s+\d+\s*week(?:s)?',         
        r'over\s+\d+\s*month(?:s)?',        
        r'\d+\s*weeks?',                     
        r'\d+\s*months?'                 
    ]
    
    frequency_matches = any(re.search(pattern, text, re.IGNORECASE) for pattern in frequency_patterns)
    
    duration_matches = any(re.search(pattern, text, re.IGNORECASE) for pattern in duration_patterns)
    
    return frequency_matches and duration_matches


def check_signed(text):
    return bool(re.search(r'(signed\s*by|signed)', text, re.IGNORECASE))

def check_patient_info(text):
    #name_present = bool(re.search(r'(name\s*:)', text, re.IGNORECASE))
    dob_present = bool(re.search(r'(DOB\s*:)', text, re.IGNORECASE))
    
    return dob_present

def check_soap_note(text):
    if not check_medicare_8_minute_rule(text):
        print("Rejected: Medicare 8-minute rule not followed (total time less than 8 minutes).")
        sys.exit(1)
    
    if not check_incorrect_billing(text):
        print("Rejected: Missing or incorrect billing detected.")
        sys.exit(1)
    
    if not check_treatment_frequency_and_duration(text):
        print("Rejected: Missing or incorrect treatment frequency/duration.")
        sys.exit(1)
    
    if not check_signed(text):
        print("Rejected: Note is not signed.")
        sys.exit(1)
    
    if not check_patient_info(text):
        print("Rejected: Missing patient information (name, DOB).")
        sys.exit(1)
    
    print("Accepted: All checks passed.")
    sys.exit(0)

soap_note_text = open("output_text.txt", "r").read()
check_soap_note(soap_note_text)
