#!/bin/bash

# Define the name of your Python script
python_script="python inference_image.py --modeldir='' --imagedir='../Face_Detect/face_detected'"

# Check if the Python script is already running
if ps aux | grep -v grep | grep "$python_script" > /dev/null; then
    echo "Script is already running."
else
    echo "Script is not running. Starting it now..."
    python3 "$python_script" &  # Run the Python script in the background
    echo "Script started."
fi
