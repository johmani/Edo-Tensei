import os
import subprocess

import ffmpeg

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


    referans = cv2.cvtColor(cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
    referans[150:930, 230:1690] = rec[0:780, 0:1460]

    input_file = 'res/full0000-1531.mp4'
    output_file = "temp/temp_" + file_name.replace("mp4", "mp4")
    width = 1920  # Replace with your desired width
    height = 1080  # Replace with your desired height
    fps = 60  # Set the desired frame rate

    process1 = (
        ffmpeg
            .input(input_file, vsync='passthrough')
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True)
    )

    process2 = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height), r=fps)
            .output(output_file, pix_fmt='yuv420p')
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )

    image_name = 0
    i = 0
    while True:
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )

        out_frame = None
        if image_name >= 787:
            points = keys[i]['points']
            in_frame = final_image(in_frame, points, referans, rec)
            i = i + 1

        process2.stdin.write(
            in_frame
            .astype(np.uint8)
            .tobytes()
        )
        image_name = image_name + 1

    process2.stdin.close()
    process1.wait()
    process2.wait()

    # for i in range(469):
    #     v = 1 - (i / 468)
    #     f = cv2.convertScaleAbs(end_frame, alpha=v, beta=0)
    #     video_writer.write(f)

    print('edit : ', "%s seconds" % (time.time() - edit_start_time))

    merge_time = time.time()

    video = "temp/temp_" + file_name
    audio = "res/f1.flac"
    res = app.config['VIDEO_DIR'] + '/' + file_name

    cmd = "ffmpeg -i " + video + " -i " + audio + " -c:v copy -map 0:v:0 -map 1:a:0 " + res
    subprocess.call(cmd, shell=True)

    if os.path.exists("temp/temp_" + file_name):
        os.remove("temp/temp_" + file_name)

    print('merge_time : ', "%s seconds" % (time.time() - merge_time))

    print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))

    return 'DONE'




