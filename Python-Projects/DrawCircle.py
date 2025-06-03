# short script that got over 99% accuracy on the draw circle game on neal.fun. adjust the constants for variables x and y (for me they were 1307 and 769 respectively) to the pixel coordinates of the central point to draw the circle around.
import math
import pyautogui
import time
import numpy as np

time.sleep(5)

for i in np.linspace(0,6,50):
    x=1307+(math.degrees(math.cos(i)))*5
    y=769+(math.degrees(math.sin(i)))*5
    pyautogui.mouseDown(x=x,y=y,button='left')

pyautogui.mouseUp()
