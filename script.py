import struct
import ctypes
import requests
import time
import os

BASE_PATH = 'D:\\Projects\\Python'
PARAMS = {
    'client_id': os.getenv('UNSPLASH_WALLPAPER_CHANGER_CID'),
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


def download_image(callback):
    """downloads and saves a random image, and then invokes the callback"""

    if PARAMS['client_id']:
        response = requests.get(
            'https://api.unsplash.com/photos/random', params=PARAMS).json()

        image_save_path = f'{BASE_PATH}\\img-{round(time.time())}.jpg'

        with open(image_save_path, 'wb') as f:
            raw_image_url = response["urls"]["raw"]
            print("Starting to download the image from url: "+raw_image_url)
            
            f.write(requests.get(raw_image_url).content)
            
            print("Downloaded the image and saved to: "+image_save_path)
        callback(image_save_path)
    else:
        print("Environment variable 'UNSPLASH_WALLPAPER_CHANGER_CID' is not set")


def change_windows_background():
    download_image(change_background)

change_windows_background()