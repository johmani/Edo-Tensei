import numpy as np
from PIL import Image
import cv2

from moviepy.editor import VideoFileClip,AudioFileClip,concatenate_videoclips
import os
import time
import warnings

from py.animator import load_interpolated_keys

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


def create_video_from_images(rec,image_folder, output_video_path, width=1920, height=1080, fps=60):

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    if not image_files:
        print("No JPG images found in the folder.")
        return
    image_files.sort()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)


    keys = load_interpolated_keys()
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)

        file_name = image_file.split(".")[0]
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        points = keys[int(file_name)]['points']
        frame = final_image(image, points,referans ,rec)

        video_writer.write(frame)

    video_writer.release()
    print(f"Video created: {output_video_path}")


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
    create_video_from_images(rec,'img', 'res/output.avi')
    print('edit : ', "%s seconds" % (time.time() - edit_start_time))

    generate_video_start = time.time()
    generate_video('static/nameplate_girl.mp4')
    print('generate video : ', "%s seconds" % (time.time() - generate_video_start))

    print('total time : ', "%s seconds" % (time.time() - total_time_start))

    return 'DONE'


# gene(cv2.imread('rec.png', cv2.IMREAD_UNCHANGED))