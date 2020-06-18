from datetime import datetime
import os
from PIL import ImageGrab
import time
import win32api
import webbrowser
from threading import Thread
from win32api import EnumDisplayMonitors

import pyautogui as ag
import PySimpleGUI as sg
THEME = 'SandyBeach'
sg.theme(THEME)

from controller import Control
from make_video import make_video
import mytoolkit


desktopPath = "C:/Users/DMHM6522/Desktop"

MAX_SCREENSHOT_SIZE = 4000000 #600 Ko
state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
if state_left == 1:
    state_left = 0

    
def capture(directory: str, filename: str, region=None, colors=True, screens=[1, 2]) -> str:
    """"""
    filename = '_'.join(filename.split('_')[1:]) # day_HH_MM_SS
        
    if not os.path.isdir(directory):
        os.mkdir(directory)
        
    path_ =f"{directory}/{filename}.png"
    
    try:
        SS = ImageGrab.grab(all_screens=True)
        if region is not None:
            print(screens)
            if screens == [1, 2]:
                sc_width, sc_height = SS.size
                region[0] = region[0] + sc_width/2
                region[2] = region[2] + sc_width/2
                left = min(region[0], region[2])
                right = max(region[0], region[2])
                upper = min(region[1], region[3])
                lower = max(region[1], region[3])
                bbox = (left, upper, right, lower)
                SS = SS.crop(bbox)
            elif screens == [1]:
                print(region)
                sc_width, sc_height = SS.size
                #region[0] = region[0] + sc_width / 2
                #region[2] = region[2] + sc_width / 2
                left = min(region[0], region[2])
                right = max(region[0], region[2])
                upper = min(region[1], region[3])
                lower = max(region[1], region[3])
                bbox = (left, upper, right, lower)
                SS = SS.crop(bbox)

        if not colors:
            SS = SS.convert(mode='L') #Grey scale
        if not os.path.isfile(path_):
            SS.save(path_)
            size_Ko = int(os.stat(path_).st_size/1000)
            if region == None:
                print(path_, f"{size_Ko} Ko", f'sc.{screens}', sep=' : ')
            else:
                print(path_, f"{size_Ko} Ko", sep=' : ')
        return path_

    except OSError or UnboundLocalError as err:
        print("Screen is locked", err, sep='\n\n')
        return None
    except SystemError as err:
        print(err)
        return None
    
def get_region_to_capture():
    """"""
    global state_left
    a = win32api.GetKeyState(0x01)
    if a == 1:
        a = 0
    currentMouseX, currentMouseY = ag.position()
    if a != state_left:  # Button state changed
        state_left = a
        if a == 0:
            end = [currentMouseX, currentMouseY]
            return "end", end
        else: #a == 1
            init = [currentMouseX, currentMouseY]
            return "init", init 
    else:
        return None, None

def get_mouse_position():
    """"""
    currentMouseX, currentMouseY = ag.position()
    return [currentMouseX, currentMouseY]

        
def start_paint(path:str)-> None:
    if path == None:
        return
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

def start_bird():
    bird_thread = Thread(target=move_mouse).start()
        
def move_mouse():
    
    try:
        bird_thread.join()
    except Exception as err:
        print(err)
    webbrowser.open("homer's bird.gif")
    webbrowser.open('notepad++')
    time.sleep(5)
    ag.write("Piou Piou", interval=0.5)
    ag.press('space') 
    

def screen_checkboxes():
    if len(EnumDisplayMonitors()) == 1:
        return sg.Checkbox("[1]", key=1, default=True), sg.Checkbox("[2]", key=2, default=False, visible=False)
    else:
        return sg.Checkbox("[1]", key=1, default=True), sg.Checkbox("[2]", key=2, default=True)

def get_n_screens(inputs):
    """"""
    screens = []
    if inputs[1]:
        screens.append(1)
    if inputs[2]:
        screens.append(2)
    return screens

def user_interface():
    layout = [
    [sg.Button('Initializing', key = 'TOGGLE AUTO CAPTURE'), *screen_checkboxes(), sg.Button('Capture', key='Capture')
     ],
    [sg.Text('', size=(2, 2), key='timer'), sg.InputText(key="Rate", size = (5,1)), sg.Button('Capture Region', key='Capture Region'),
     sg.Checkbox("Paint", key='Viewer', default=True), sg.Button("Bird", key='MouseMover', visible=True)],
    [sg.Text(key="Last Image", size=(20, 1)),  sg.Checkbox("Colors", key="Colors", default=False)],
    [sg.Button('Exit', key='Exit')],
          ]

    window = sg.Window("Activity Report", layout,
                       keep_on_top=True,
                       grab_anywhere=True,
                       #no_titlebar=True,
                       return_keyboard_events=True)
    last_capture = ""
    #Initializing Control
    control = Control()
    control.start()
    MouseMover = False

    startMousePosition = []
    endMousePosition = []
    capturing_region = False
    while True:
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime("%y-%m-%d_%a_%H-%M-%S")
        Day = formatted_timestamp.split('_')[0]
        
        if not capturing_region :
            event, inputs = window.Read(timeout=800) #Most of the time
        elif capturing_region:
            event, inputs = window.Read(1) #We lower the timeout to avoid lag when getting Mouse coordinates while Capturing Region
        if control.state:
            window['TOGGLE AUTO CAPTURE'].Update('Auto-capture : ON', button_color=("white", "green"))
            
        if event in (None, 'Exit'):
            break

        elif event == 'TOGGLE AUTO CAPTURE' and not control.state:
            control.start()
            window['TOGGLE AUTO CAPTURE'].Update('Auto-capture : ON', button_color=("white", "green"))
            
        elif event == 'TOGGLE AUTO CAPTURE' and control.state:
            control.stop()
            window['TOGGLE AUTO CAPTURE'].Update("Auto-capture : OFF", button_color=("white", "red"))

        elif event == 'Capture':
            path_to_screenshot = capture(desktopPath, formatted_timestamp)
            if inputs['Viewer'] == True:
                start_paint(path_to_screenshot)
            
        elif event == "Capture Region":
            capturing_region= True
            window["Capture Region"].Update("Select region", button_color=("white", "orange"))


               
        if capturing_region:
            if not startMousePosition:
                step, value = get_region_to_capture()
                if step == 'init':
                    startMousePosition = value
                    endMousePosition = []
            else:
                step, value = get_region_to_capture()
                if step == 'end':
                    endMousePosition = value
                    capturing_region= False
                    window["Capture Region"].Update("Capture Region",
                                                    button_color=sg.LOOK_AND_FEEL_TABLE[THEME]['BUTTON'])

        """if capturing_region:
            if event.startswith('Mouse') and startMousePosition == []:
                startMousePosition = get_mouse_position()
                endMousePosition = []
            elif event.startswith('Mouse'):
                endMousePosition = get_mouse_position()
                capturing_region= False
                window["Capture Region"].Update("Capture Region",
                                                    button_color=sg.LOOK_AND_FEEL_TABLE[THEME]['BUTTON'])"""
        
        if startMousePosition != [] and endMousePosition != []:
            screens = get_n_screens(inputs)
            bbox = startMousePosition + endMousePosition
            #(0, 0, 3840, 1080)
            startMousePosition = []
            endMousePosition = []
            time.sleep(1)
            path_to_screenshot = capture(desktopPath, formatted_timestamp, region=bbox, screens=screens)
            if inputs['Viewer'] == True:
                start_paint(path_to_screenshot)
            
        if control.state and timestamp.second == 1 and login_screen(f"screenshots/{Day}"):
            control.stop()

    #-------------- Capture every minute --------------------
        #if control.state and timestamp.second in [0, 10, 20, 30, 40, 50]: 
        if control.state and timestamp.second == 0:
            screens = get_n_screens(inputs)

            if inputs["Colors"]:
                last_capture = capture(f"screenshots/{Day}", formatted_timestamp, screens=screens)
            else:
                last_capture = capture(f"screenshots/{Day}", formatted_timestamp, colors=False, screens=screens)
            
            try:
                window['Last Image'].Update(last_capture.split('/')[-1])
            except AttributeError:
                pass

    #--------------- Mouse mover -----------------------
        if event == "MouseMover" :
            MouseMover = not MouseMover

        if MouseMover:
            window.Elem("MouseMover").Update(button_color=('white', 'red'))
        else:
            window.Elem("MouseMover").Update(button_color=sg.LOOK_AND_FEEL_TABLE['SandyBeach']['BUTTON'])

            

        if MouseMover and timestamp.second in [0, 30]:
            start_bird()

    #---------------- Timer -----------------------------#
        window.Elem('timer').Update(timestamp.second)
        
    #-------------- Build Video ------------------------------
        if timestamp.hour == 18 and not os.path.isfile(f"./videos/{Day}.avi"):
            pass
            #make_video(Day)
    return window


if __name__ == '__main__':
    window = user_interface()
    window.close()
