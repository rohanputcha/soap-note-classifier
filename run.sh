#!/bin/bash

./clear.sh
python3 pdfToImages.py
python3 imagesToText.py
if [ $? -ne 0 ]; then
    echo "Error setting up PDF parsing."
    exit 1
fi
python3 autofailParser.py
if [ $? -ne 0 ]; then
    echo "Autofail condition met, program will terminate."
    exit 1
fi
python3 llmParser.py
