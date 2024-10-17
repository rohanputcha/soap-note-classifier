import re

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
    total_time = extract_time(text)
    if total_time < 8:
        return False  # Reject if total time is less than 8 minutes
    return True

def check_incorrect_billing(text):
    """
    Check for common billing codes and ensure they seem logical.
    You could refine this by looking for inconsistencies in CPT codes or 'units' logic.
    """
    billing_matches = re.findall(r'(CPT\s*code|units|billing|charged)', text, re.IGNORECASE)
    
    if not billing_matches:
        return False  # If no billing information is provided, it's an issue.

    # Further validation logic could go here, for now, we assume if billing exists, it's valid
    return True

import re

def check_treatment_frequency_and_duration(text):
    """
    A more lenient check for treatment frequency and duration to account for various ways
    it could be written, allowing for more flexibility in the patterns matched.
    """
    # Looser frequency patterns (e.g., "1 time per week", "1x weekly", "once a week")
    frequency_patterns = [
        r'\d+\s*x\s*/?\s*week',                  # e.g., "1x/week" or "2 x per week"
        r'\d+\s*times?\s*/?\s*(per|a)?\s*week',  # e.g., "1 time per week", "2 times a week"
        r'once\s*(per)?\s*week',                 # e.g., "once per week"
        r'weekly'                                # e.g., "weekly"
    ]
    
    # Looser duration patterns (e.g., "for 4 weeks", "for 3 weeks", "for 1 month", "over 6 weeks")
    duration_patterns = [
        r'for\s+\d+\s*week(?:s)?',               # e.g., "for 4 weeks"
        r'for\s+\d+\s*month(?:s)?',              # e.g., "for 2 months"
        r'over\s+\d+\s*week(?:s)?',              # e.g., "over 2 weeks"
        r'over\s+\d+\s*month(?:s)?',             # e.g., "over 3 months"
        r'\d+\s*weeks?',                         # e.g., "4 weeks" without "for"
        r'\d+\s*months?'                         # e.g., "2 months" without "for"
    ]
    
    # Look for frequency
    frequency_matches = any(re.search(pattern, text, re.IGNORECASE) for pattern in frequency_patterns)
    
    # Look for duration
    duration_matches = any(re.search(pattern, text, re.IGNORECASE) for pattern in duration_patterns)
    
    # If either frequency or duration is found (being lenient to pass), return True
    return frequency_matches and duration_matches


def check_signed(text):
    """
    Check if the note is signed. In real cases, signatures are often mentioned as 'Signed by'.
    """
    return bool(re.search(r'(signed\s*by|signed)', text, re.IGNORECASE))

def check_patient_info(text):
    """
    Check if patient information is present. In the case of redaction, we will only check
    for the existence of the field (e.g., 'Name', 'DOB').
    """
    #name_present = bool(re.search(r'(name\s*:)', text, re.IGNORECASE))
    dob_present = bool(re.search(r'(DOB\s*:)', text, re.IGNORECASE))
    
    return dob_present

def check_soap_note(text):
    """
    The main function to run all checks on a SOAP note.
    Any failure results in rejection.
    """
    if not check_medicare_8_minute_rule(text):
        return "Rejected: Medicare 8-minute rule not followed (total time less than 8 minutes)."
    
    if not check_incorrect_billing(text):
        return "Rejected: Incorrect billing detected."
    
    if not check_treatment_frequency_and_duration(text):
        return "Rejected: Missing or incorrect treatment frequency/duration."
    
    if not check_signed(text):
        return "Rejected: Note is not signed."
    
    if not check_patient_info(text):
        return "Rejected: Missing patient information (name, DOB)."
    
    return "Accepted: All checks passed."

# Example usage
soap_note_text = open("output_text.txt", "r").read()  # Replace with your file path
result = check_soap_note(soap_note_text)
print(result)
