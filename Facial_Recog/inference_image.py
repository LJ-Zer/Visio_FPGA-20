import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
import datetime
import shutil  # Import the shutil module for file operations

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True, default='')
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--imagedir', help='Name of the folder containing images to perform detection on. Folder must contain only images.',
                    required=True, default='../Face_Detect/face_detected')
parser.add_argument('--save_results', help='Save labeled images and annotation data to a results folder',
                    action='store_true')
parser.add_argument('--noshow_results', help='Don\'t show result images (only use this if --save_results is enabled)',
                    action='store_false')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

# Parse user inputs
MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels

min_conf_threshold = float(args.threshold)
use_TPU = args.edgetpu

save_results = args.save_results  # Defaults to False
show_results = args.noshow_results  # Defaults to True

IM_DIR = args.imagedir

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If the user has specified the name of the .tflite file, use that name, otherwise use the default 'edgetpu.tflite'
    if GRAPH_NAME == 'detect.tflite':
        GRAPH_NAME = 'edgetpu.tflite'

# Get path to the current working directory
CWD_PATH = os.getcwd()

# Define path to images and grab all image filenames
PATH_TO_IMAGES = os.path.join(CWD_PATH, IM_DIR)
images = glob.glob(PATH_TO_IMAGES + '/*.jpg') + glob.glob(PATH_TO_IMAGES + '/*.png') + glob.glob(PATH_TO_IMAGES + '/*.bmp')

# Create results directory if the user wants to save results
if save_results:
    RESULTS_DIR = IM_DIR + '_results'
    RESULTS_PATH = os.path.join(CWD_PATH, RESULTS_DIR)
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for the label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# The first label is '???', which has to be removed.
if labels[0] == '???':
    del labels[0]

# Load the TensorFlow Lite model
# If using Edge TPU, use the special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

save_folder1 = 'Face-Detected'  # Folder name to store captured images
if not os.path.exists(save_folder1):
    os.makedirs(save_folder1)

lord_john_perucho_counter = 0

outname = output_details[0]['name']

if 'StatefulPartitionedCall' in outname:  # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else:  # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2


processed_images = set()
processed_images_folder = 'processed_images'  # Folder name for processed images
if not os.path.exists(processed_images_folder):
    os.makedirs(processed_images_folder)

while True:
# Loop over every image and perform detection
    for image_path in images:
        # Check if the image has already been processed
        if image_path in processed_images:
            continue  # Skip this image, as it has already been processed

        # Load image and resize to the expected shape [1xHxWx3]
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects
        
        for i in range(len(scores)):
            if 0 <= int(classes[i]) < len(labels) and (scores[i] > min_conf_threshold) and (scores[i] <= 1.0):
                object_name = labels[int(classes[i])]  # Look up object name from the "labels" array using the class index
                
                if object_name == "Lord John Perucho":
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")  # YYYY-MM-DD_HH-MM-SS format
                    ymin = int(max(1, (boxes[i][0] * imH)))
                    xmin = int(max(1, (boxes[i][1] * imW)))
                    ymax = int(min(imH, (boxes[i][2] * imH)))
                    xmax = int(min(imW, (boxes[i][3] * imW)))
                    cropped_image = image[ymin:ymax, xmin:xmax]

                    # Resize the cropped image to the desired size (320x320)
                    cropped_image_resized = cv2.resize(cropped_image, (320, 320))

                    # Save the resized cropped image
                    image_name = f"{timestamp}_{object_name} ({lord_john_perucho_counter}).jpg"
                    image_path_processed = os.path.join(save_folder1, image_name)
                    cv2.imwrite(image_path_processed, cropped_image_resized)  # Capture the frame
                    print("Resized and cropped image captured and saved!")
                    lord_john_perucho_counter += 1
                    
                    # .Move the processed image to the processed_images folder
                    shutil.move(image_path, os.path.join(processed_images_folder, os.path.basename(image_path)))
                    processed_images.add(image_path)


    # Clean up
    cv2.destroyAllWindows()