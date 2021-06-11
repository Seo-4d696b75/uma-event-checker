import pyautogui
import cv2
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders
import sys
import re

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

ocr = tools[0]
print(f"OCR tool: {ocr.get_name()}")

def get_window():
    left = pyautogui.locateOnScreen('template/header_left.png', confidence=0.8)
    if left is None:
        return None
    right = None
    for p in pyautogui.locateAllOnScreen('template/header_right.png', confidence=0.95):
        if abs(p.top - left.top) < 5:
            right = p
            break
    if right is None:
        return None
    x = left.left
    y = left.top
    width = (right.left - left.left) + right.width
    height = int(width * 1.857685)
    return pyautogui.screenshot(region=(x,y,width,height))
    
def locate_window():
    left = pyautogui.locateOnScreen('header_left.png', confidence=0.8)
    if left is None:
        return None
    right = None
    for p in pyautogui.locateAllOnScreen('header_right.png', confidence=0.95):
        if abs(p.top - left.top) < 5:
            right = p
            break
    if right is None:
        return None
    width = (right.left - left.left) + right.width
    return (left.left, left.top, width)

def get_str(left,top,width):
    img = crop_event_title(left,top,width)
    return extract_str(img,width)

def crop_event_title(left, top, width):
    x = left + int(width * 0.16)
    y = top + 44 + int(width * 0.33)
    w = int(width * 0.55)
    h = int(width * 0.065)
    return pyautogui.screenshot(region=(x,y,w,h))
    
    
def extract_str(img, width=None):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    if width is not None:
        # 才能開花によるイベントには勝負服のアイコンが先頭にあるので除去
        x = round(width * 0.01)
        s = gray[0:gray.shape[0], x:(x+2)]
        h, w = s.shape
        rows = 0
        for y in range(h):
            v = 0
            for x in range(w):
                v += s[y,x]
            if v > w * 200:
                rows += 1
        if rows >= h * 0.6:
            gray = gray[0:gray.shape[0], int(width*0.065):gray.shape[1]]
    resized = cv2.resize(gray, (gray.shape[1]*2, gray.shape[0]*2), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("gray.png", resized)
    _, th = cv2.threshold(resized, 220, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("2.png", th)
    txt = ocr.image_to_string(
        Image.fromarray(th),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=7)
    )
    return re.sub('[\s　]+', '', txt)