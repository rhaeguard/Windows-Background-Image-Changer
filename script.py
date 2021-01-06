import struct
import ctypes
import requests
import time
import os
import sys

if not os.getenv('WBC_IMAGES_DIR'):
    sys.exit('Environment variable WBC_IMAGES_DIR is not set')

if not os.getenv('WBC_UNSPLASH_CID'):
    sys.exit("Environment variable 'WBC_UNSPLASH_CID' is not set")

IMAGES_DIR = os.environ["WBC_IMAGES_DIR"]

PARAMS = {
    'client_id': os.environ['WBC_UNSPLASH_CID'],
    'orientation': "landscape",
    'query': "nature"
}

SPI_SETDESKWALLPAPER = 20
IS_64_BIT = struct.calcsize('P') == 8

def change_background(path):
    """Change background depending on bit size"""

    # struct is a module for packing and unpacking data to and from C representations.
    # P represents void * (a generic pointer).
    # On 32-bit systems a pointer is 4 bytes, and on a 64-bit system a pointer requires 8 bytes.
    # struct.calcsize('P') calculates the number of bytes required to store a single pointer
    # -- returning 4 on a 32-bit system and 8 on a 64-bit system.

    if IS_64_BIT:
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(
            SPI_SETDESKWALLPAPER, 0, path, 3)
    print("Background picture changed")

def get_image_url():
    """downloads and saves a random image, and then invokes the callback"""
    try:
        response = requests.get('https://api.unsplash.com/photos/random', params=PARAMS).json()
        return response["urls"]["raw"]
    except requests.exceptions.ConnectionError as _:
        sys.exit("Could not establish a connection to get an image URL")

def download_image(callback):
    image_save_path = os.path.join(IMAGES_DIR, f'img-{round(time.time())}.jpg')

    with open(image_save_path, 'wb') as f:
        raw_image_url = get_image_url()
        print(f'Starting to download the image from url: {raw_image_url}')

        try:
            f.write(requests.get(raw_image_url).content)
            print(f'Downloaded the image and saved to: {image_save_path}')
        except requests.exceptions.ConnectionError as _:
            sys.exit("Could not establish a connection to download the image")
    
    callback(image_save_path)

def change_windows_background():
    download_image(change_background)

change_windows_background()
