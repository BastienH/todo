# Code to check where left button is pressed and released
import win32api
import time
import pyautogui as ag
"""
def 
state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

while True:
    a = win32api.GetKeyState(0x01)
    b = win32api.GetKeyState(0x02)

    if a != state_left:  # Button state changed
        state_left = a
        currentMouseX, currentMouseY = ag.position()
        if a < 0:
            print('Left Button Pressed')
            print(currentMouseX, currentMouseY)
            init_X, init_Y = currentMouseX, currentMouseY
        else:
            print('Left Button Released')
            print(currentMouseX, currentMouseY)
            end_X, end_Y = currentMouseX, currentMouseY
            return init_X, init_Y, end_X, end_Y

    if b != state_right:  # Button state changed
        state_right = b
        print(b)
        if b < 0:
            print('Right Button Pressed')
        else:
            print('Right Button Released')
    time.sleep(0.01)"""

def get_region_to_capture():
    """
        Change mouse image
        #Grey out screen
        #Listen for click
        #Get click 1 position
        #Show movement from initial click
        #Listen for click
        #Get click 2 position
    """
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            currentMouseX, currentMouseY = ag.position()
            if a < 0:
                print('Left Button Pressed')
                print(currentMouseX, currentMouseY)
                init_X, init_Y = currentMouseX, currentMouseY
            else:
                print('Left Button Released')
                print(currentMouseX, currentMouseY)
                end_X, end_Y = currentMouseX, currentMouseY
                bbox = init_X, init_Y, end_X, end_Y
                break
        time.sleep(0.001)
    return bbox

bbox = get_region_to_capture()
