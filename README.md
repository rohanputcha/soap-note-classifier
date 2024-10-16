# soap-note-classifier

# Current goal

- Focus on auto-fail criteria:
  - Medicare 8-minute rule
  - Incorrect billing
  - Not specifying treatment frequency and duration
  - Wildly different treatment vs diagnosis
  - A note that is not signed
  - Not identifying relevant pt info (name, DOB)

# Setup

Run the following code to set up:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 extractPdf.py
python3 extractPdf.py2
```
