#!/bin/bash

# Clear previous data or setup
./clear.sh

# Run the Python scripts sequentially
python extractPdf.py
python extractPdf2.py
python llmParser.py
