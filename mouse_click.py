import win32api, win32con
import pyautogui as ag
import time

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
if state_left == 1:
    state_left = 0

    
def get_region_to_capture2():
    """"""
    global state_left
    count = 0
    while True:
        a = win32api.GetKeyState(0x01)
        if a == 1: #This because a is randomly 1 or 0, so we make if constantly 0
            a = 0
        if a != state_left:  # Button state changed
            count += 1
            state_left = a #Capture new state
        if count == 2: #The second time the state changes (button up), we get the position
            currentMouseX, currentMouseY = ag.position()
            return [currentMouseX, currentMouseY]

get_region_to_capture2()
