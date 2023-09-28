import os
import subprocess
from flaskServer import app
from py.animator import load_interpolated_keys
from PIL import Image
import numpy as np
import time
import cv2
import warnings
# import matplotlib.pyplot as plt
import  multiprocessing as mp

def final_image(frame, points, referans, rec):
    referans[150:930, 230:1690] = rec[0:780, 0:1460]
    source_points = np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]])
    destination_points = np.float32(points)
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
    warped_referans = cv2.warpPerspective(referans, perspective_matrix, (1920, 1080))

    frontImage = Image.fromarray(warped_referans)
    background = Image.fromarray(frame)
    background.paste(frontImage, (0, 0), frontImage)
    image_np = np.array(background)

    return image_np

def apply(path,name,start_index,rec):
    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
    keys = load_interpolated_keys()

    video_writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    video_writer.set(cv2.CAP_PROP_BITRATE, 100)
    video_capture = cv2.VideoCapture(path)
    index = start_index

    print(start_index, ",", path)
    while video_capture.isOpened():

        ret, frame = video_capture.read()

        if not ret:
            break
        points = keys[index]['points']
        frame = final_image(frame, points, referans, rec)
        video_writer.write(frame)
        index = index + 1

    video_capture.release()
    video_writer.release()


def gene(rec,file_name):
    print("start")

    total_time_start = time.time()

    p1 = mp.Process(target=apply, args=('res/p2/0000-0372.mp4',"temp/_1_" + file_name, 0, rec))
    p2 = mp.Process(target=apply, args=('res/p2/0373-0744.mp4',"temp/_2_" + file_name, 373, rec))


    p1.start()
    p2.start()

    video_writer = cv2.VideoWriter("temp/end_" + file_name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    end_frame = cv2.imread('res/0744.jpg', cv2.IMREAD_UNCHANGED)
    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
    keys = load_interpolated_keys()
    points = keys[744]['points']
    end_frame = final_image(end_frame, points, referans, rec)
    for i in range(469):
        v = 1 - (i / 468)
        f = cv2.convertScaleAbs(end_frame, alpha=v, beta=0)
        video_writer.write(f)
    video_writer.release()

    p1.join()
    p2.join()


    files = ["c.mp4", "_1_" + file_name,"_2_" + file_name,"end_" + file_name]
    txt_file = "temp/"+ file_name +"_t.txt"
    with open(txt_file, "w") as file:
        for f in files:
            file.write("file '" + f + "'\n")

    video = "temp/temp_" + file_name
    audio = "res/f.flac"
    res = app.config['VIDEO_DIR'] + '/' + file_name

    cmd = "ffmpeg -f concat -safe 0 -i " + txt_file + " -c copy " + video
    subprocess.call(cmd, shell=True)

    cmd = "ffmpeg -i " + video + " -i " + audio + " -c:v copy -map 0:v:0 -map 1:a:0 " + res
    subprocess.call(cmd, shell=True)

    if os.path.exists(txt_file):
        os.remove(txt_file)
    if os.path.exists(video):
        os.remove(video)
    if os.path.exists("temp/_1_" + file_name):
        os.remove("temp/_1_" + file_name)
    if os.path.exists("temp/_2_" + file_name):
        os.remove("temp/_2_" + file_name)
    if os.path.exists("temp/end_" + file_name):
        os.remove("temp/end_" + file_name)

    print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))






