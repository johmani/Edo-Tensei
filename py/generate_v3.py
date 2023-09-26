import os

from moviepy.editor import VideoFileClip, AudioFileClip
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

    video_writer = cv2.VideoWriter("temp/temp_" + file_name.replace("mp4", "avi"), cv2.VideoWriter_fourcc(*'XVID'), 60, (1920, 1080))
    video_writer.set(cv2.CAP_PROP_BITRATE, 10000000)  # Set a higher bitrate
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


    # cmd = "ffmpeg -i res/f.flac -i res/output.avi -c:v libx264 -crf 18 -preset slow -c:a aac -strict experimental -ac 2 -channel_layout stereo -pix_fmt yuv420p res/final.mp4 -r 60"
    # subprocess.call(cmd, shell=True)

    merge_time = time.time()


    video_clip = VideoFileClip("temp/temp_" + file_name.replace("mp4", "avi"))
    audio_clip = AudioFileClip( "res/f.flac")
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(app.config['VIDEO_DIR'] + '/' + file_name, codec='libx264')

    audio_clip.close()
    video_clip.close()

    if os.path.exists("temp/temp_" + file_name):
        os.remove("temp/temp_" + file_name)

    print('merge_time : ', "%s seconds" % (time.time() - merge_time))

    print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))

    return 'DONE'


