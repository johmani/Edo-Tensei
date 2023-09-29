from py.animator import load_interpolated_keys
import  multiprocessing as mp
from flaskServer import app
from PIL import Image
import numpy as np
import subprocess
import time
import cv2
import os

import warnings

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

def process(path,name,start_index,rec):
    print("start new process")

    total_time_start = time.time()
    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
    keys = load_interpolated_keys()

    video_writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    video_writer.set(cv2.CAP_PROP_BITRATE, 256)
    video_capture = cv2.VideoCapture(path)
    index = start_index

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

    print(f'process {start_index} : ', "%s seconds" % (time.time() - total_time_start))


def final_scene(file_name,rec):

    video_writer = cv2.VideoWriter("temp/end_" + file_name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    video_writer.set(cv2.CAP_PROP_BITRATE, 256)
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

def combine(file_name):
    hard_time_start = time.time()

    files = ["c.mp4", "_1_" + file_name, "_2_" + file_name, "end_" + file_name]
    txt_file = "temp/" + file_name + "_t.txt"
    with open(txt_file, "w") as file:
        for f in files:
            file.write("file '" + f + "'\n")

    audio = "res/f.flac"
    res = app.config['VIDEO_DIR'] + '/' + file_name

    cmd = f"ffmpeg -f concat -safe 0 -i {txt_file} -i {audio} -c:v copy -c:a aac {res}"
    subprocess.call(cmd, shell=True)

    # cmd = f'ffmpeg -i {f} -vf "scale={1440}:{720}" -c:a copy ' + res
    # subprocess.call(cmd, shell=True)

    if os.path.exists(txt_file):
        os.remove(txt_file)
    if os.path.exists("temp/_1_" + file_name):
        os.remove("temp/_1_" + file_name)
    if os.path.exists("temp/_2_" + file_name):
        os.remove("temp/_2_" + file_name)
    if os.path.exists("temp/end_" + file_name):
        os.remove("temp/end_" + file_name)
    if os.path.exists(f):
        os.remove(f)
    if os.path.exists("temp/temp_rec_" + file_name.replace('mp4','png')):
        os.remove("temp/temp_rec_" + file_name.replace('mp4','png'))

    print('hard_time : ', "%s seconds" % (time.time() - hard_time_start))

def gene(rec,file_name):

    print("start")
    yield f"data: {0}\n\n"

    total_time_start = time.time()

    p1 = mp.Process(target=process, args=('res/p2/0000-0372.mp4', "temp/_1_" + file_name, 0, rec))
    p2 = mp.Process(target=process, args=('res/p2/0373-0744.mp4', "temp/_2_" + file_name, 373, rec))

    p1.start()
    yield f"data: {5}\n\n"
    p2.start()
    yield f"data: {10}\n\n"

    final_scene(file_name, rec)

    yield f"data: {30}\n\n"

    p1.join()
    yield f"data: {60}\n\n"
    p2.join()
    yield f"data: {95}\n\n"

    combine(file_name)
    yield f"data: {100}\n\n"

    print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))









