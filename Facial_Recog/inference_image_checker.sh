#!/bin/bash

# Check if the Python script is already running
if ps aux | grep -v grep | grep "python inference_image.py --modeldir='' --imagedir='../Face_Detect/face_detected'" > /dev/null; then
    echo "Script is already running."
else
    echo "Script is not running. Starting it now..."
    python inference_image.py --modeldir='' --imagedir='../Face_Detect/face_detected' &  # Run the Python script in the background
    echo "Script started."
fi
