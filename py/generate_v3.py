import os
import subprocess
from flaskServer import app
from py.animator import load_interpolated_keys
from PIL import Image
import numpy as np
import time
import cv2
import warnings
warnings.filterwarnings('ignore')

def final_image(orginal_image, points, referans,rec):


    source_points = np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]])
    destination_points = np.float32(points)
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
    warped_referans = cv2.warpPerspective(referans, perspective_matrix, (1920, 1080))

    frontImage = Image.fromarray(cv2.cvtColor(warped_referans, cv2.COLOR_BGRA2RGBA))
    background = Image.fromarray(cv2.cvtColor(orginal_image, cv2.COLOR_BGRA2RGBA))
    background.paste(frontImage, (0, 0), frontImage)
    image_np = np.array(background)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)

    return image_np


def gene(rec,file_name):
    print("start")

    total_time_start = time.time()
    edit_start_time = time.time()
    keys = load_interpolated_keys()

    image_name = 0
    i = 0

    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
    video_capture = cv2.VideoCapture('res/full0000-1531.mp4')

    referans[150:930, 230:1690] = rec[0:780, 0:1460]

    video_writer = cv2.VideoWriter("temp/temp_" + file_name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    # video_writer.set(cv2.CAP_PROP_BITRATE, 10000000)  # Set a higher bitrate
    end_frame = None
    while video_capture.isOpened():

        ret, frame = video_capture.read()
        if not ret:
            break
        if image_name >= 787 :
            points = keys[i]['points']
            frame = final_image(frame, points, referans, rec)
            i = i + 1
        video_writer.write(frame)
        image_name = image_name + 1

        end_frame = frame

    for i in range(469):
        v = 1 - (i / 468)
        f = cv2.convertScaleAbs(end_frame, alpha=v, beta=0)
        video_writer.write(f)


    video_capture.release()
    video_writer.release()
    print('edit : ', "%s seconds" % (time.time() - edit_start_time))

    merge_time = time.time()

    video = "temp/temp_" + file_name
    audio = "res/f.flac"
    res =  app.config['VIDEO_DIR'] + '/' + file_name

    # cmd = "ffmpeg -i " + video + " -i " + audio + " -c:v copy -map 0:v:0 -map 1:a:0 " + res

    cmd = "ffmpeg -i " + video + " -i " + audio + " " + res
    subprocess.call(cmd, shell=True)

    # out = app.config['VIDEO_DIR'] + '/' + file_name
    # cmd = "ffmpeg -i " + res + " " + out
    # subprocess.call(cmd, shell=True)


    if os.path.exists("temp/temp_" + file_name):
        os.remove("temp/temp_" + file_name)


    print('merge_time : ', "%s seconds" % (time.time() - merge_time))


    print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))

    return 'DONE'


