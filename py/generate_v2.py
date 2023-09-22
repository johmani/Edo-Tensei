from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,ImageSequenceClip
from py.animator import load_interpolated_keys
from PIL import Image
import numpy as np
import time
import cv2
import warnings
warnings.filterwarnings('ignore')



def final_image(orginal_image, points, referans,rec):

    referans[150:930, 230:1690] = rec[0:780, 0:1460]
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


def gene(rec):
    total_time_start = time.time()
    edit_start_time = time.time()
    keys = load_interpolated_keys()
    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
    video_capture = cv2.VideoCapture('res/cuted0000-0744.mp4')

    new_clip = []
    image_name = 0
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        points = keys[image_name]['points']
        frame = final_image(frame, points, referans, rec)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        new_clip.append(frame)
        image_name = image_name + 1
    video_capture.release()
    print('edit : ', "%s seconds" % (time.time() - edit_start_time))

    generate_video_start = time.time()

    new_clip = ImageSequenceClip(new_clip,fps=60)

    clip1 = VideoFileClip("res/clip1.mp4")
    new_clip = new_clip.subclip(0, 20.9)
    new_clip = new_clip.fadeout(7)
    audio = AudioFileClip("res/a1.flac")
    new_clip = new_clip.set_audio(audio)
    final_video = concatenate_videoclips([clip1, new_clip])
    final_video.write_videofile('res/nameplate_girl.mp4')

    clip1.close()
    new_clip.close()
    final_video.close()

    print('generate video : ', "%s seconds" % (time.time() - generate_video_start))
    print('total time : ', "%s seconds" % (time.time() - total_time_start))


