import cv2
import json
import pyautogui
import numpy as np
import os

data = json.load(open('icon.json', 'r', encoding='utf-8'))

support_icons = [cv2.imread(f"icon/{d['i']}") for d in data['support']]


def read_chara_icon(d):
    i = d['i']
    icons = [cv2.imread(f"icon/{i}")]
    name = i[0:(len(i)-4)]
    i_e = f"icon/{name}_e.png"
    if os.path.exists(i_e):
        icons.append(cv2.imread(i_e))
    return icons


chara_icons = [read_chara_icon(d) for d in data['chara']]


def compare_template(img, icon, w):
    scale = w / icon.shape[1]
    h = round(scale * icon.shape[0])
    template = cv2.resize(icon, (w, h))
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val


def compare_event_img(img, template, width):
    scale = width / 546.0
    size = (int(template.shape[1]*scale), int(template.shape[0]*scale))
    resized = cv2.resize(template, size)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray.png", gray)
    _, gray = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    #print(gray.shape, resized.shape)
    cv2.imwrite("th.png", gray)
    res = cv2.matchTemplate(gray, resized, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #print(max_val, max_loc)
    return max_val


def detect_chara_name(img, width):
    w = round(width * 0.131429)
    def calc(icons): return max(
        [compare_template(img, icon, w) for icon in icons])
    score = [calc(icons) for icons in chara_icons]
    v = max(score)
    idx = score.index(v)
    d = data['chara'][idx]
    print(f"max-score:{v}", d)
    return d['n']


def detect_support_name(img, width):
    w = round(width * 0.1120)
    score = [compare_template(img, icon, w) for icon in support_icons]
    v = max(score)
    idx = score.index(v)
    d = data['support'][idx]
    print(f"max-score:{v}", d)
    return d['n']


event_chara = cv2.imread('template/event_chara.png', cv2.IMREAD_GRAYSCALE)
event_support = cv2.imread('template/event_support.png', cv2.IMREAD_GRAYSCALE)
event_main = cv2.imread('template/event_main.png', cv2.IMREAD_GRAYSCALE)

def detect_event_type(left, top, width):
    x = left + int(width * 0.1557)
    y = top + 44 + int(width * 0.2950)
    w = int(width * 0.3640)
    h = int(width * 0.0311)
    img_event = np.array(pyautogui.screenshot(region=(x, y, w, h)))
    img_event = cv2.cvtColor(img_event, cv2.COLOR_RGB2BGR)
    if compare_event_img(img_event, event_chara, width) > 0.7:
        return 'chara'
    elif compare_event_img(img_event, event_support, width) > 0.7:
        return 'support'
    elif compare_event_img(img_event, event_main, width) > 0.7:
        return 'main'
    else:
        print("fial to detect event type")
        return None


def detect_name(left, top, width, type):
    if type == 'chara':
        x = left + int(width * 0.0190)
        y = top + 44 + int(width * 0.2762)
        size = int(width * 0.1428)
        img = np.array(pyautogui.screenshot(region=(x, y, size, size)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return detect_chara_name(img, width)
    elif type == 'support':
        x = left + int(width * 0.0256)
        y = top + 44 + int(width * 0.2619)
        w = int(width * 0.1318)
        h = int(width * 0.1684)
        img = np.array(pyautogui.screenshot(region=(x, y, w, h)))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return detect_support_name(img, width)
    elif type == 'main':
        return "URA"
    else:
        print("type is None")
        return None
