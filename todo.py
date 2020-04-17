from datetime import datetime
import json
import os
#import psutil
import sys

import PySimpleGUI as sg
from pyperclip import copy

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

# --------- Get list of ongoing projects ---------------#
CODE_BASE = r"C:\Users\DMHM6522\CodeBase" #This has to be configured for each user
PROJECTS = [d for d in os.listdir(CODE_BASE) if os.path.isdir(os.path.join(CODE_BASE, d))]

#Credit to aminusfu : https://github.com/cherrypy/cherrypy/blob/0857fa81eb0ab647c7b59a019338bab057f7748b/cherrypy/process/wspbus.py#L305
startup_cwd = os.getcwd() #Used in do_execv, to swap between projects

#------------- Context Manager ------------#
    
try: #If started from COMMAND, user can choose his directory directly
    SELECTED_DIR = sys.argv[1]
except IndexError:
    SELECTED_DIR = ''

#If no system argument is provided, provide GUI to choose
if SELECTED_DIR == '':
    #One radio button for each project
    #Generates a list of lists so the display is vertical
    radio_buttons = [[sg.Radio(dir_name, 'Projects', key=dir_name)] for dir_name in PROJECTS] 

    prompt_layout= [
        *radio_buttons, #Note the unpacking
        [sg.Button('Open')],
        [sg.Text(key='-INFO-', size=(20,1))],
        ]

    prompt_window = sg.Window('Select your project', prompt_layout, location=(80, 500),)

    while True:
        event, values = prompt_window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Open':
            for k, v in values.items():
                if v:
                   SELECTED_DIR = k
                   prompt_window.close()
                else:
                    prompt_window.Elem('-INFO-').Update('Please select a project')

SELECTED_DIR_FULL_PATH = os.path.join(CODE_BASE, SELECTED_DIR)

# -----------------Main ----------- #
os.chdir(SELECTED_DIR_FULL_PATH)#This is crucial, as it sets the working directory, and the whole content.

TODO_DIR = os.path.join(os.getcwd(), "todo")
if not os.path.isdir(TODO_DIR):
    os.mkdir(TODO_DIR)

TODO_FILE = r"./todo/todo_list.txt"
DONE_FILE = r"./todo/done_list.txt"

ARCHIVE_DIR = os.path.join(os.getcwd(), "todo", "archive")
if not os.path.isdir(ARCHIVE_DIR):
    os.mkdir(ARCHIVE_DIR)
    
WIDTH = 25
HEIGHT = 7

def do_execv(event):
    """Re-execute the current process.
    This must be called from the main thread, because certain platforms
    (OS X) don't allow execv to be called in a child thread very well.
    """
    args = sys.argv[:1] #In our implementation, we only want the first arg
    args.append(event) # And we add user selection (project name)
    print('Re-spawning %s' % ' '.join(args))
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.chdir(startup_cwd)
    os.execv(sys.executable, args)
    
def debug(text):
    window.Element('debug').Update(text)

# --------------- IO -----------------------
def write_to_file(input_ :list, filename:str)->str:
    """returns the input_ string if wrote successfully, else returns None"""
    with open(filename, 'w+', encoding='utf-8') as file:
        for i in input_:
            print(i, file=file)
    return input_

def read_(filename)->list:
    #Create empty file if it doesn't exist
    if not os.path.isfile(filename):
        open(filename, 'a').close()
    #Read file content to list
    with open(filename, 'r+', encoding='utf-8') as f:
        data = f.readlines()
    data= [i.strip() for i in data]
    for i, v in enumerate(data):
        if v == '\r\n':
            data.pop(i)
    return data

done_list = read_(DONE_FILE)
todo_list = read_(TODO_FILE)

#---------- Add and remove from lists ---------------        
def add_text_to_list(input_key:str, list_key:str):
    """Add the input text to the associated list, """
    list_values = window.Element(list_key).get_list_values()

    new_item = window.Element(input_key).get()
    window.Element(input_key).Update("")

    if new_item != "":
        list_values.append(new_item)
    window.Element(list_key).Update(values=list_values) 

def move_from_list_to_list(item:str, list_A_key:str, list_B_key:str):

    list_A = window.Elem(list_A_key).get_list_values()   
    list_B = window.Elem(list_B_key).get_list_values()

    if item in list_A:
        list_A.remove(item)
    list_B.append(item)

    window.Elem(list_A_key).Update(values=list_A)
    window.Elem(list_B_key).Update(values=list_B)

# ------ Menu Definition ------ #      
menu_def = [['Go to', PROJECTS],
            ['Help', 'About...'], ]
    
# ------ GUI Defintion ------ #      

layout = [
    [sg.Menu(menu_def, )],
    [sg.Text(SELECTED_DIR, font=15, background_color = sg.LOOK_AND_FEEL_TABLE["DarkTeal12"]["BACKGROUND"] ),],
    [sg.Frame("To do", [
        [sg.Listbox(values=todo_list, key="todo_list",
                size=(WIDTH, HEIGHT),
                no_scrollbar=True,
                #font=("Times New Roman", 12),
                enable_events=True, 
                right_click_menu=['&Right', ["Done", "Copy", "Delete"]],
                background_color='white',
                )],
        [sg.InputText(key="input_text_todo", size=(25, 1))],
        ],
        font = 15,
        background_color='orange',
        element_justification='right',
        title_color='dark blue',
        title_location=sg.TITLE_LOCATION_TOP_RIGHT,
        )],

    
    [sg.Frame('Done', [
        [sg.Listbox(values=done_list, key="done_list",
                size=(WIDTH, HEIGHT),
                no_scrollbar=True,
                enable_events=True,
                right_click_menu=['&Right', ["Copy", "Delete", "Todo", "Archive list"]],
                background_color='white',
                )], 
        [sg.InputText(key="input_text_done", size=(25, 1))],
        ],
        font = 15,
        title_color='dark blue',
        background_color='light green',
        title_location=sg.TITLE_LOCATION_TOP_RIGHT,
        #element_justification='right' 
    )],
    
    [sg.OK('add', key="add_item", visible=False)], #add_ext_ is the key for event handling
    [sg.Button('Save', key='Save'), sg.Button('Safe Exit', key='Safe Exit'), sg.Button('Open Folder', key=os.getcwd())],
    [sg.Multiline('debugger', key="debug", size=(WIDTH, 2))],
          ]

sg.theme('DarkTeal12')
window = sg.Window("*** TO DO ***",
                   layout,
                   keep_on_top=True,
                   #grab_anywhere=True,
                   no_titlebar=True,
                   return_keyboard_events=True,
                   resizable=True,
                   location=(80, 500),
                   )

#---------- 
while True:
    event, inputs = window.Read()
    if event in (None, 'Exit'):
        break
    
    if event == "Safe Exit":
        write_to_file(done_list, DONE_FILE)
        write_to_file(todo_list, TODO_FILE)
        break
    if event == "Save":
        write_to_file(done_list, DONE_FILE)
        write_to_file(todo_list, TODO_FILE)
        
    '''if len(event) > 1 and not event.startswith("Mouse"):
        print(event)
        print('\n')'''
            
#----------- Changing Project ------------#
    if event in PROJECTS:
        write_to_file(done_list, DONE_FILE)
        write_to_file(todo_list, TODO_FILE)
        window.close()
        do_execv(event)
        
#---------- Pressing Enter------------
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):       # Check for ENTER key
        elem = window.FindElementWithFocus()                            # go find element with Focus
        if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:       # if it's a button element, click it
            elem.Click()
            print("button clicked")
            
    if event == "add_item":
        add_text_to_list("input_text_todo", "todo_list")
        write_to_file(todo_list, TODO_FILE)
        add_text_to_list("input_text_done", "done_list")
        write_to_file(done_list, DONE_FILE)

#----------Right click events ----------     
    if event == "Copy":
        key = window.FindElementWithFocus().Key #Where the click happened
        copy(window.Element(key).get()[0])

       #debug("failed to copy")
            
    if event == "Delete":
        key = window.FindElementWithFocus().Key
        print(key)
        try:
            selected = window.Element(key).get()[0]
            list_ = window.Element(key).get_list_values()
            list_.remove(selected)
            window.Element(key).Update(values=list_)
        except:
            debug("Failed to delete, probably no element selected")

    if event == "Done":
        item = window["todo_list"].get()[0]
        move_from_list_to_list(item, "todo_list", "done_list")
        
    if event == "Todo":
        item = window.Element("done_list").get()[0]
        move_from_list_to_list(item, "done_list", "todo_list")

    if event == "Archive list":
        key = window.FindElementWithFocus().Key
        try:
            list_ = window[key].get_list_values()
            archive_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M')
            archive_path = os.path.join(ARCHIVE_DIR, f"{archive_datetime}.txt")
            write_to_file(list_, archive_path)
            debug("Archive created")
            window[key].Update([])
        except Exception as err:
            debug(f'Failed to archive:{err}')

    if event == os.getcwd():
        os.system(f"start explorer {os.getcwd()}")

window.close()
