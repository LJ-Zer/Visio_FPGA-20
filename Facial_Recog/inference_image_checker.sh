#!/bin/bash

# Define the name of your Python script
python_script="python"
script_args="inference_image.py --modeldir='' --imagedir='../Face_Detect/face_detected'"

# Check if the Python script is already running
if ps aux | grep -v grep | grep "$python_script $script_args" > /dev/null; then
    echo "Script is already running."
else
    echo "Script is not running. Starting it now..."
    $python_script $script_args &  # Run the Python script in the background
    echo "Script started."
fi
