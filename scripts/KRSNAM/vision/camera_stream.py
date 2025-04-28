import cv2
import requests
import numpy as np

def fetch_image_from_esp32_cam(url='http://192.168.4.1/capture'):
    try:
        # print("Try block eecuted successfully")
        image_resp = requests.get(url)
        image_array = bytearray(image_resp.content) 
        image_np = cv2.imdecode(np.asarray(image_array, dtype=np.uint8), -1)
        return image_np
    except:
        return None
