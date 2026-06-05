import cv2
import numpy as np
import pyttsx3
from tkinter import *
from tkinter import filedialog

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

# --- Preprocessing with Canny + Threshold ---
def preprocess_image(img):
    # Blur to reduce noise
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Canny edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Dilate edges to make dots thicker
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)

    return dilated

# --- Detect Braille Dots ---
def detect_braille_cells(processed_img, original_img):
    contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of Contours = ", len(contours))

    dots = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 5 < w < 50 and 5 < h < 50:  # filter small/large noise
            cx, cy = x + w // 2, y + h // 2
            dots.append((cx, cy))
            cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detected Dots', original_img)
    cv2.waitKey(0)

    # Sort dots by Y first (top to bottom), then X (left to right)
    dots = sorted(dots, key=lambda p: (p[1], p[0]))
    return dots

# --- Classify Braille ---
def classify_braille(dots):
    grid = [0, 0, 0, 0, 0, 0]
    for i, (x, y) in enumerate(dots[:6]):  # Only take first 6 dots
        grid[i] = 1
    return braille_dict.get(tuple(grid), '?')

# --- Text-to-Speech ---
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---- Main Execution ----
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("Pick the image files", "*.png;*.jpg;*.jpeg")])
root.destroy()

print("Selected file:", file_path)

# Read the input image
img = cv2.imread(file_path, 0)
cv2.imshow('Input Image', img)
cv2.waitKey(0)

# Resize for consistency
img = cv2.resize(img, (256, 256))

# Preprocess with Canny
processed = preprocess_image(img)
cv2.imshow('Processed (Canny + Threshold)', processed)
cv2.waitKey(0)

# Detect contours (dots)
original_colored = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
patterns = detect_braille_cells(processed, original_colored)
print("Dot positions:", patterns)

# Classify Braille
text = classify_braille(patterns)
print("Detected text:", text)

# Speak result
speak_text("Character")
speak_text(text)
