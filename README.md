# Setup
1. Add your SOAP note to the project directory.

2. Make a ```config.py``` file, and enter the following fields:

```API_KEY="<YOUR OWN API KEY>"```

Replace <YOUR API KEY> with the actual Gemini API key

```SOAP_NOTE_PATH="<PATH TO SOAP NOTE>"```

Replace <PATH TO SOAP NOTE> with your actual path to the SOAP you want to check. 
In most IDEs, if you drag the file from the explorer to your terminal you will see the file's absolute path. Only include the path after ```soap-note-classifier/```.

3. Run the following commands to set up:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

4. Run the following command to execute the evaluator:

```
bash ./run.sh
```