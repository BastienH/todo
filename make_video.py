import cv2
import numpy as np
import glob
import os

def make_video(date:str):
    """Takes all images in the ./screenshots/{date} directory and builds a video with them in the video directory"""
    img_array = []
    dirfiles = glob.glob(f'./screenshots/{date}/*.png')
    
    if dirfiles == []:
        print('Empty or wrong directory')
        return
    
    print(f'Start reading files for {date}...')
    for filename in glob.glob(f'./screenshots/{date}/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
     
    print('Start making video...')
    out = cv2.VideoWriter(f'./videos/{date}.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])

    print('Start release...')
    out.release()

    os.system(f"start ./videos/{date}.avi")
