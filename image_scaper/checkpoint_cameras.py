#!/usr/bin/env python

import requests, os, shutil, signal, time, random
import pandas as pd
import numpy as np

# set directory name
directory = input("Please insert path to destination folder: ")
# /Users/llemonthyme/Desktop/test

# set hours for procedure (timeout is in seconds)
hours = int(input("Please enter duration to run scraper (in hours): "))
timeout = 3600 * hours 

# make folders for images
for foldername in ['4703','4713','2701','2702']: 
    folder = os.path.join(directory, foldername)
    if os.path.isdir(folder) == False:
        os.mkdir(os.path.join(directory, foldername))

# define a handler for the timeout
def handler(signum, frame):
    raise Exception(f"Download complete. End of {timeout} seconds.")

def download_images():
    print("downloading...")
    while True:
        results = requests.get("https://api.data.gov.sg/v1/transport/traffic-images").json()
        cameras = results['items'][0]['cameras']
        for camera in cameras:
            # 4 checkpoint cameras
            for camera_id in ['4703','4713','2701','2702']:          
                if camera['camera_id'] == camera_id:
                    # get image url
                    url = camera['image']
                    # get timestamp
                    timestamp = camera['timestamp'].split('+')[0]
                    # download from image url
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        with open(os.path.join(directory, f"{camera_id}/{camera_id}_{timestamp}.jpg"), 'wb') as file:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, file)       
        # wait 60 seconds before sending next request
        time.sleep(60)

# register the signal function handler
signal.signal(signal.SIGALRM, handler)

# set alarm for function end
signal.alarm(timeout)

try:
    download_images()
except Exception as exc: 
    print (exc)