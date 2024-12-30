# -*- coding: utf-8 -*-
"""Pcos-detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/pcos-detection-f57075c5-df00-4fd5-88ab-fb4213d62c61.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240519/auto/storage/goog4_request%26X-Goog-Date%3D20240519T052335Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D03f4b68d19a908fff2c5d439672e1acaec18c17d349f21b741d9d9a528a86151b9e9a3655651982f4e703940903700167998397d4543987d83b8f329d76521cbcbfe836ac51ebe8ebab73e2661f6293cb35b5afba9b1d4216246b85abbb4b99b11b2213cd68f1bcbdd2ed708a4d8e154439c40cc92d5977face519a0ea78dccd71ad79cd67b98fb55d052b765b398975ae42d02dc6904faab3569e047f5df11a6f5f3ee0e0c03c3c9917ab5ee054875fba036f0c95a592918126148f0e930e3f17286bc86df40f58c32ab2b268bf80aff617d4a698bafa961cb73f912f101cd61000d29662949674f37546759af0d3964d957df965f581dd353b7adf104399c0
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'pcos234:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F5034497%2F8448576%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240519%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240519T052335Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D430c54e5ba25ca45a313ce7d375c6934e95fada20ca64f8140fad9067e4f5994f62da5fbafb059ecc32ad12bfb0352611e83cf262edcc41325780c09041fa86eb88810542c504e69f43c16972cbc5d597273e341c0dcfee359f2272b700e56a4b4acf4d1ce253b7dd9d6f433d2fed3afc21d6932e1c9d510e1db94b7f357489ae83b7c511bdf0d924486341fe785e29c19cb2157ee7d92ad390b55cd2fd9bc099413cd72a56da6e5bd72d73ea1bed95276fb4709b15748f4be1b261d8fc72481ebe7a47b5763c1a0087e48e2429ce918431257e4a6af4143062988eed89153c82f26f5170a9e725e0a1b4d67e954972149cba47064be7831a3537c9310994dc8'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

! nvidia-smi -L



# Commented out IPython magic to ensure Python compatibility.
# %%time
# ! pip install --upgrade ultralytics -qq

import ultralytics
print(ultralytics.__version__)

import warnings
warnings.filterwarnings("ignore")


import re
import glob
import random
import yaml
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns

import IPython.display as display
from PIL import Image
import cv2

from ultralytics import YOLO

pip install wandb



class CFG:
    DEBUG = False
    FRACTION = 0.05 if DEBUG else 1.0
    SEED = 88

    # classes
    CLASSES = ['no-pcos', 'pcos']
    NUM_CLASSES_TO_TRAIN = len(CLASSES)

    # training
    EPOCHS = 3 if DEBUG else 10 # 100
    BATCH_SIZE = 4

    BASE_MODEL = 'yolov8x' # yolov8n, yolov8s, yolov8m, yolov8l, yolov8x, yolov9c, yolov9e, yolo_nas_s, yolo_nas_m, yolo_nas_l
    BASE_MODEL_WEIGHTS = f'{BASE_MODEL}.pt'
    EXP_NAME = f'yolov8x{EPOCHS}_epochs'

    OPTIMIZER = 'Adam' # SGD, Adam, Adamax, AdamW, NAdam, RAdam, RMSProp, auto
    LR = 1e-5
    LR_FACTOR = 0.001
    WEIGHT_DECAY = 0.0005
    DROPOUT = 0.2
    PATIENCE = 10
    PROFILE = False
    LABEL_SMOOTHING = 0.0

    # paths
    CUSTOM_DATASET_DIR = '/kaggle/input/pcos234'
    OUTPUT_DIR = './'

dict_file = {
    'train': os.path.join(CFG.CUSTOM_DATASET_DIR, 'train'),
    'val': os.path.join(CFG.CUSTOM_DATASET_DIR, 'valid'),
    'test': os.path.join(CFG.CUSTOM_DATASET_DIR, 'test'),
    'nc': CFG.NUM_CLASSES_TO_TRAIN,
    'names': CFG.CLASSES
    }

with open(os.path.join(CFG.OUTPUT_DIR, 'data.yaml'), 'w+') as file:
    yaml.dump(dict_file, file)

### read yaml file created
def read_yaml_file(file_path = CFG.CUSTOM_DATASET_DIR):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print("Error reading YAML:", e)
            return None

### print it with newlines
def print_yaml_data(data):
    formatted_yaml = yaml.dump(data, default_style=False)
    print(formatted_yaml)

file_path = os.path.join(CFG.OUTPUT_DIR, 'data.yaml')
yaml_data = read_yaml_file(file_path)

if yaml_data:
    print_yaml_data(yaml_data)

def display_image(image, print_info = True, hide_axis = False):
    if isinstance(image, str):  # Check if it's a file path
        img = Image.open(image)
        plt.imshow(img)
    elif isinstance(image, np.ndarray):  # Check if it's a NumPy array
        image = image[..., ::-1]  # BGR to RGB
        img = Image.fromarray(image)
        plt.imshow(img)
    else:
        raise ValueError("Unsupported image format")

    if print_info:
        print('Type: ', type(img), '\n')
        print('Shape: ', np.array(img).shape, '\n')

    if hide_axis:
        plt.axis('off')

    plt.show()

example_image_path = '/kaggle/input/pcos234/train/images/img_0_1033_jpg.rf.e837430c9bd50f29559ffa3eb5b938ef.jpg'
display_image(example_image_path, print_info = True, hide_axis = False)

def get_image_properties(image_path):
    # Read the image file
    img = cv2.imread('/kaggle/input/pcos234/train/images/img_0_1033_jpg.rf.e837430c9bd50f29559ffa3eb5b938ef.jpg')

    # Check if the image file is read successfully
    if img is None:
        raise ValueError("Could not read image file")

    # Get image properties
    properties = {
        "width": img.shape[1],
        "height": img.shape[0],
        "channels": img.shape[2] if len(img.shape) == 3 else 1,
        "dtype": img.dtype,
    }

    return properties

img_properties = get_image_properties(example_image_path)
img_properties

# Commented out IPython magic to ensure Python compatibility.
# %%time
# class_idx = {str(i): CFG.CLASSES[i] for i in range(CFG.NUM_CLASSES_TO_TRAIN)}
# 
# class_stat = {}
# data_len = {}
# class_info = []
# 
# for mode in ['train', 'valid', 'test']:
#     class_count = {CFG.CLASSES[i]: 0 for i in range(CFG.NUM_CLASSES_TO_TRAIN)}
# 
#     path = os.path.join(CFG.CUSTOM_DATASET_DIR, mode, 'labels')
# 
#     for file in os.listdir(path):
#         with open(os.path.join(path, file)) as f:
#             lines = f.readlines()
# 
#             for cls in set([line[0] for line in lines]):
#                 class_count[class_idx[cls]] += 1
# 
#     data_len[mode] = len(os.listdir(path))
#     class_stat[mode] = class_count
# 
#     class_info.append({'Mode': mode, **class_count, 'Data_Volume': data_len[mode]})
# 
# dataset_stats_df = pd.DataFrame(class_info)
# dataset_stats_df

# Create subplots with 1 row and 3 columns
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot vertical bar plots for each mode in subplots
for i, mode in enumerate(['train', 'valid', 'test']):
    sns.barplot(
        data=dataset_stats_df[dataset_stats_df['Mode'] == mode].drop(columns='Mode'),
        orient='v',
        ax=axes[i],
        palette='Set2'
    )

    axes[i].set_title(f'{mode.capitalize()} Class Statistics')
    axes[i].set_xlabel('Classes')
    axes[i].set_ylabel('Count')
    axes[i].tick_params(axis='x', rotation=90)

    # Add annotations on top of each bar
    for p in axes[i].patches:
        axes[i].annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', fontsize=8, color='black', xytext=(0, 5),
                         textcoords='offset points')

plt.tight_layout()
plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for mode in ['train', 'valid', 'test']:
#     print(f'\nImage sizes in {mode} set:')
# 
#     img_size = 0
#     for file in glob.glob(os.path.join(CFG.CUSTOM_DATASET_DIR, mode, 'images', '*')):
# 
#         image = Image.open(file)
# 
#         if image.size != img_size:
#             print(f'{image.size}')
#             img_size = image.size
#             print('\n')



CFG.BASE_MODEL_WEIGHTS

import torch
model = YOLO(CFG.BASE_MODEL_WEIGHTS)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

print('Model: ', CFG.BASE_MODEL_WEIGHTS)
print('Epochs: ', CFG.EPOCHS)
print('Batch: ', CFG.BATCH_SIZE)

model = YOLO(CFG.BASE_MODEL_WEIGHTS)





# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# ### train
# model.train(
#     data=os.path.join(CFG.OUTPUT_DIR, 'data.yaml'),
#     task='detect',
#     imgsz=(img_properties['height'], img_properties['width']),
#     epochs=CFG.EPOCHS,
#     batch=CFG.BATCH_SIZE,
#     optimizer=CFG.OPTIMIZER,
#     lr0=CFG.LR,
#     lrf=CFG.LR_FACTOR,
#     weight_decay=CFG.WEIGHT_DECAY,
#     dropout=CFG.DROPOUT,
#     fraction=CFG.FRACTION,
#     patience=CFG.PATIENCE,
#     profile=CFG.PROFILE,
#     label_smoothing=CFG.LABEL_SMOOTHING,
#     name=f'{CFG.BASE_MODEL}_{CFG.EXP_NAME}',
#     seed=CFG.SEED,
#     val=True,
#     amp=True,
#     exist_ok=True,
#     resume=False,
#     device=0, # Set to single GPU device
#     verbose=False,
# )

# Commented out IPython magic to ensure Python compatibility.
img_properties
# Export the model
model.export(
    format = 'onnx', # openvino, onnx, engine, tflite
    imgsz = (img_properties['height'], img_properties['width']),
    half = False,
    int8 = False,
    simplify = False,
    nms = False,
)
results_paths = [
    i for i in
    glob.glob(f'{CFG.OUTPUT_DIR}runs/detect/{CFG.BASE_MODEL}_{CFG.EXP_NAME}/*.png') +
    glob.glob(f'{CFG.OUTPUT_DIR}runs/detect/{CFG.BASE_MODEL}_{CFG.EXP_NAME}/*.jpg')
    if 'batch' not in i
]

results_paths
# %matplotlib inline
# Loading the best performing model
model = YOLO('/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/weights/best.pt')

metrics = model.val(data='/kaggle/working/data.yaml', split = 'test')

example_image_path = '/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/val_batch1_pred.jpg'
display_image(example_image_path)

# Import the necessary libraries
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Load the best performing model
model = YOLO('/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/weights/best.pt')

# Path to your test image
image_path = '/kaggle/input/pcos234/test/images/pco_4_jpg.rf.6fd0a62e06a0a87288a6b4c754b40d53.jpg'

# Run inference on the single image
results = model.predict(source=image_path, save=False, show=False)

# Get the first result (assuming one image)
result = results[0]

# Convert the result to an OpenCV image
result_image = result.plot()

# Convert BGR image to RGB for displaying with Matplotlib
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

# Display the image with detections
plt.imshow(result_image_rgb)
plt.axis('off')  # Hide axes
plt.show()

# Import the necessary libraries
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Load the best performing model
model = YOLO('/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/weights/best.pt')

# Path to your test image
image_path = '/kaggle/input/pcos234/test/images/pco_8_jpg.rf.915e3e663ddde584151479ff93aae822.jpg'

# Run inference on the single image
results = model.predict(source=image_path, save=False, show=False)

# Get the first result (assuming one image)
result = results[0]

# Convert the result to an OpenCV image
result_image = result.plot()

# Convert BGR image to RGB for displaying with Matplotlib
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

# Display the image with detections
plt.imshow(result_image_rgb)
plt.axis('off')  # Hide axes
plt.show()

# Import the necessary libraries
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Load the best performing model
model = YOLO('/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/weights/best.pt')

# Path to your test image
image_path = '/kaggle/input/pcos234/test/images/img_0_114_jpg.rf.ea6075be6764b1f5920d5d9453a13a27.jpg'

# Run inference on the single image
results = model.predict(source=image_path, save=False, show=False)

# Get the first result (assuming one image)
result = results[0]

# Convert the result to an OpenCV image
result_image = result.plot()

# Convert BGR image to RGB for displaying with Matplotlib
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

# Display the image with detections
plt.imshow(result_image_rgb)
plt.axis('off')  # Hide axes
plt.show()

from IPython.display import Image

# Path to the image
image_path = '/kaggle/working/runs/detect/yolov8x_yolov8x10_epochs/val_batch1_pred.jpg'

# Display the image
Image(filename=image_path)
