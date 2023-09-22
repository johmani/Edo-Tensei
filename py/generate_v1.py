import time
import cv2
from PIL import Image
import numpy as np
from py.animator import load_interpolated_keys
from moviepy.editor import VideoFileClip,AudioFileClip,concatenate_videoclips
import warnings
warnings.filterwarnings('ignore')


def final_image(orginal_image, points, referans_image,rec):
    referans = cv2.imread(referans_image, cv2.IMREAD_UNCHANGED)


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

def edit_vedio(rec,output_video_path, width=1920, height=1080, fps=60):

    keys = load_interpolated_keys()
    video_capture = cv2.VideoCapture('res/cuted0000-0744.mp4')

    image_name = 0

    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
    video_writer.set(cv2.CAP_PROP_BITRATE, 10000000)  # Set a higher bitrate
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        points = keys[image_name]['points']
        frame = final_image(frame, points, 'res/referans11.png', rec)

        video_writer.write(frame)
        image_name = image_name + 1


    video_writer.release()
    video_capture.release()

def generate_video(output_path):
    clip1 = VideoFileClip("res/clip1.mp4")
    output = VideoFileClip("res/output.avi").subclip(0, 20.9)
    output = output.fadeout(7)

    audio = AudioFileClip("res/a1.flac")

    output = output.set_audio(audio)

    final_video = concatenate_videoclips([clip1, output])
    final_video.write_videofile(output_path)

    clip1.close()
    output.close()


def gene(rec):
    print('start')
    total_time_start = time.time()
    edit_start_time = time.time()


    edit_vedio(rec, 'res/output.avi')

    print('edit : ', "%s seconds" % (time.time() - edit_start_time))

    generate_video_start = time.time()
    generate_video('static/nameplate_girl.mp4')
    print('generate video : ', "%s seconds" % (time.time() - generate_video_start))

    print('total time : ', "%s seconds" % (time.time() - total_time_start))

    return 'DONE'


# gene(cv2.imread('rec.png', cv2.IMREAD_UNCHANGED))

