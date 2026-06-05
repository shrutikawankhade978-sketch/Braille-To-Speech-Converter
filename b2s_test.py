import cv2
import numpy as np
import pyttsx3
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
from imutils import contours
import imutils
from skimage import io
import os,time
import warnings

# Braille pattern to English character dict mapping
braille_dict = {
    (1, 0, 0, 0, 0, 0): 'A',
    (1, 1, 0, 0, 0, 0): 'B',
    (1, 0, 0, 1, 0, 0): 'C',
    (1, 0, 0, 1, 1, 0): 'D',
    (1, 0, 0, 0, 1, 0): 'E',
    (1, 1, 0, 1, 0, 0): 'F',
    (1, 1, 0, 1, 1, 0): 'G',
    (1, 1, 0, 0, 1, 0): 'H',
    (0, 1, 0, 1, 0, 0): 'I',
    (0, 1, 0, 1, 1, 0): 'J',
    (1, 0, 1, 0, 0, 0): 'K',
    (1, 1, 1, 0, 0, 0): 'L',
    (1, 0, 1, 1, 0, 0): 'M',
    (1, 0, 1, 1, 1, 0): 'N',
    (1, 0, 1, 0, 1, 0): 'O',
    (1, 1, 1, 1, 0, 0): 'P',
    (1, 1, 1, 1, 1, 0): 'Q',
    (1, 1, 1, 0, 1, 0): 'R',
    (0, 1, 1, 1, 0, 0): 'S',
    (0, 1, 1, 1, 1, 0): 'T',
    (1, 0, 1, 0, 0, 1): 'U',
    (1, 1, 1, 0, 0, 1): 'V',
    (0, 1, 0, 1, 1, 1): 'W',
    (1, 0, 1, 1, 0, 1): 'X',
    (1, 0, 1, 1, 1, 1): 'Y',
    (1, 0, 1, 0, 1, 1): 'Z',
}

def preprocess_image(img):
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

def detect_braille_cells(thresh_img):
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of Contours = ", len(contours))
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', img)
    cv2.waitKey(0)

    dots = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        print(x,y,w,h)
        if 5 < w < 250 and 5 < h < 250:  # filter likely dots
            cx, cy = x + w//2, y + h//2
            dots.append((cx, cy))

    # print(dots)

    # Sort and group dots into 2x3 grids
    dots = sorted(dots, key=lambda p: (p[1], p[0]))  # sort top to bottom, then left to right
    # print(dots)

    return dots

def classify_braille(dots):
    # Assume dots are in 2x3 grid order
    grid = [0, 0, 0, 0, 0, 0]

    for i, (x, y) in enumerate(dots):
        if i < 6:
            grid[i] = 1  # Mark detected dots

    return braille_dict.get(tuple(grid), '?')


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---- Main Execution ----
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Pick the image files", "*.png")])
root.destroy()

print(file_path)

image_path = file_path

## Read the input image
img = cv2.imread(image_path,0)
cv2.imshow('Test Input Image',img)
cv2.waitKey(0)

img = cv2.resize(img, (256, 256))
thresh = preprocess_image(img)
cv2.imshow('Preprocess Image',img)
cv2.waitKey(0)
cv2.imshow('Thresh Image',thresh)
cv2.waitKey(0)

patterns = detect_braille_cells(thresh)
print(patterns)

text = classify_braille(patterns)

print("Detected text:", text)

speak_text("Character ")
speak_text(text)