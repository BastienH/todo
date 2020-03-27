from time import sleep

import pyautogui as ag

while True:
    currentMouseX, currentMouseY = ag.position()
    ag.moveTo(currentMouseX+25, currentMouseY+25)
    ag.moveTo(currentMouseX+50, currentMouseY+50)
    ag.moveTo(currentMouseX, currentMouseY)
    print('moved')
    sleep(60*4)
    
