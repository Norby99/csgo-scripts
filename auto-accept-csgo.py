import cv2
import numpy as np
import pyautogui
from urllib.request import urlopen
from PIL import Image
import json

class AutoAccept:

    def __init__(self):
        with open('setup.json') as f:
            self.data = json.load(f)
        
        imageURL = self.data['auto-accept-images'][self.data['language']]
        self.img_accept_mm = cv2.cvtColor(np.array(Image.open(urlopen(imageURL))), cv2.COLOR_BGR2GRAY)
        
    def get_screenshot(self):
        return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)

    def compare_images(self):
        w, h = self.img_accept_mm.shape[::-1]
        res = cv2.matchTemplate(self.get_screenshot(), self.img_accept_mm, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
            
        for pt in zip(*loc[::-1]):
            self.coordinates = (pt[0]+w/2, pt[1]+h/2)
            return True

    def click_accept(self):
        pyautogui.click(self.coordinates)
            
if __name__ == "__main__":
    a = AutoAccept()
    while True:
        if a.compare_images() == True:
            a.click_accept()
            break
    exit()
