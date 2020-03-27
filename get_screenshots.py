from datetime import datetime
import os
from PIL import ImageGrab
import time

import pyautogui as ag
import PySimpleGUI as sg
THEME = 'SandyBeach'
sg.theme(THEME)


from controller import Control
from make_video import make_video
import mytoolkit


desktopPath = "C:/Users/DMHM6522/Desktop"

MAX_SCREENSHOT_SIZE = 600000 #600 Ko

def capture(directory:str, filename:str, greyscale=True) -> str:
    
    filename = '_'.join(filename.split('_')[1:]) # day_HH_MM_SS
        
    if not os.path.isdir(directory):
        os.mkdir(directory)
        
    path_ =f"{directory}/{filename}.png"
    
    try:
        SS = ImageGrab.grab(all_screens=True)
        if greyscale:
            SS = SS.convert(mode='L')
        SS.save(path_)
        print(path_)
        return path_

    except OSError or UnboundLocalError:
        print("Screen is locked")
        return None
    

def start_paint(path:str)-> None:
    path = path.replace('/', '\\')
    os.system(f"start %windir%\\system32\\mspaint.exe \"{path}\"")

    
def login_screen(path:str)-> bool:
    """checks if the latest modified file is larger than 500ko, meaning its a login screen"""
    latest_file = mytoolkit.get_latest_file_in_dir(path)
    file_size = os.stat(latest_file).st_size
    if file_size > MAX_SCREENSHOT_SIZE: 
         return True
    else:
        return False

def move_mouse():
    currentMouseX, currentMouseY = ag.position()
    try:
        ag.moveTo(currentMouseX+20, currentMouseY)
        ag.moveTo(currentMouseX+30, currentMouseY)
    except ag.FailSafeException:
        ag.moveTo(currentMouseX-20, currentMouseY)
        ag.moveTo(currentMouseX-30, currentMouseY)
    
    ag.moveTo(currentMouseX, currentMouseY)
         
layout = [
    [sg.Button('Start', key = 'START'), sg.Button('Stop', key='STOP'), sg.Button('Capture', key='Capture'), sg.Button('MouseMover', key='MouseMover')],
    [sg.Text(key="State", size=(10, 1)), sg.Text('', size=(10, 2) justification='right', key='timer')],
    [sg.Text(key="Last Image", size=(20, 1))],
    [sg.Button('Exit', key='Exit')],
          ]

window = sg.Window("Activity Report", layout, keep_on_top=True, grab_anywhere=True, no_titlebar=True)
control = Control()
MouseMover = False

while True:
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%y-%b-%d_%a_%H-%M-%S")
    Day = formatted_timestamp.split('_')[0]
    
    event, inputs = window.Read(timeout=800)
    if event in (None, 'Exit'):
        break

    elif event == 'START' and not control.state:
        control.start()
        window['State'].Update("Running")
        
    elif event == 'STOP' and control.state:
        control.stop()
        window['State'].Update("Stopped")

    elif event == 'Capture':
        path_to_screenshot = capture(desktopPath, formatted_timestamp, greyscale=False)
        start_paint(path_to_screenshot)
        
    if control.state and timestamp.second == 1 and login_screen(f"screenshots/{Day}"):
        control.stop()
        window['State'].Update("Stopped")
    
#--------------- Mouse mover -----------------------
    if event == "MouseMover" :
        MouseMover = not MouseMover

    if MouseMover:
        window.Elem("MouseMover").Update(button_color=('white', 'red'))
    else:
        window.Elem("MouseMover").Update(button_color=sg.LOOK_AND_FEEL_TABLE['SandyBeach']['BUTTON'])

    if MouseMover and timestamp.second == 30:
        move_mouse()
#-------------- Capture every minute --------------------
    if control.state and timestamp.second == 0:

        capture(f"screenshots/{Day}", formatted_timestamp)
        
        window['Last Image'].Update(formatted_timestamp)

#---------------- Timer -----------------------------#
    window.Elem('timer').Update(timestamp.second)
#-------------- Build Video ------------------------------
    if timestamp.hour == 18 and not os.path.isfile(f"./videos/{Day}.avi"):
        make_video(Day)

window.close()
