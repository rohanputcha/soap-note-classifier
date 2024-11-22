#!/bin/bash

# Clear previous data or setup
./clear.sh

# Run the Python scripts sequentially
python pdfToImages.py
python imagesToText.py
python llmParser.py
