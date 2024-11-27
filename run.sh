#!/bin/bash

# Clear previous data or setup
./clear.sh

# Run the Python scripts sequentially
python3 pdfToImages.py
python3 imagesToText.py
python3 llmParser.py
