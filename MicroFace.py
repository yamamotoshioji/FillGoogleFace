import os
import sys
import requests
import cv2
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v3.1/analyze"

data_dir_path = u"./data_dir"
data_save_path= u"./data_save"
file_list = os.listdir(r'./data_dir/')
file_save_list = os.listdir(r'./data_save/')
   
for file_name in file_list:
    if file_name != '.DS_Store':
        root, ext = os.path.splitext(file_name)
        if ext == u'.png' or u'.jpeg' or u'.jpg':
            abs_name = data_dir_path + '/' + file_name
            image = cv2.imread(abs_name)
# Set image_path to the local path of an image that you want to analyze.
# Sample images are here, if needed:
# https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images
            image_path = abs_name

# Read the image into a byte array
            image_data = open(image_path, "rb").read()
            headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                       'Content-Type': 'application/octet-stream'}
            params = {'visualFeatures': 'Categories,Description,Color'}
            response = requests.post(
                analyze_url, headers=headers, params=params, data=image_data)
            response.raise_for_status()

            # The 'analysis' object contains various fields that describe the image. The most
            # relevant caption for the image is obtained from the 'description' property.
            analysis = response.json()
            #print(analysis)
            image_caption = analysis["description"]["captions"][0]["text"].capitalize()

            # Display the image and overlay it with the caption.
            image = Image.open(BytesIO(image_data))
            plt.imshow(image)
            plt.axis("off")
            _ = plt.title(image_caption, size="x-large", y=-0.1)
            #plt.show()
            #print(file_name,analysis['categories'][0]['score'])
            data = file_name + str(analysis['categories'][0]['score'])
            file = "data,txt"
            fileobj = open(file, "a", encoding = "utf_8")
            fileobj.write(data + '\n')
