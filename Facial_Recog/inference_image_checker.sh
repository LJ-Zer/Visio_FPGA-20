#!/bin/bash

# Define the name of your Python script and its arguments
python_script="python inference_image.py --modeldir='' --imagedir='../Face_Detect/face_detected'"

# Function to check if the Python script is running
check_script() {
    ps aux | grep -v grep | grep "$python_script" > /dev/null
}

# Loop to continuously check and run the script if it's not already running
while true; do
    if check_script; then
        echo "Script is already running."
    else
        echo "Script is not running. Starting it now..."
        $python_script &  # Run the Python script in the background
        echo "Script started."
    fi
    sleep 60  # Sleep for 60 seconds before checking again
done
