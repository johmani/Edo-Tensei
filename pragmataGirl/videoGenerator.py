import json

from pragmataGirl.animator import load_interpolated_keys
import  multiprocessing as mp
from PIL import Image
import numpy as np
import subprocess
import time
import cv2
import os


def final_image(frame, points,referans,rec):
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


def process(input_path, result_path,referans,rec,keys,start_index,state_path):
    print("start new process")

    video_writer = cv2.VideoWriter(result_path, cv2.VideoWriter_fourcc(*'mp4v'), 60, (1920, 1080))
    video_writer.set(cv2.CAP_PROP_BITRATE, 256)
    video_capture = cv2.VideoCapture(input_path)
    index = start_index

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        with open(state_path, 'r') as file:
            task_state = json.load(file)['state']
        if task_state:
            break

        points = keys[index]['points']
        frame = final_image(frame, points,referans,rec)
        video_writer.write(frame)
        index = index + 1

    video_capture.release()
    video_writer.release()


class VideoGenerator:
    def __init__(self,dirctory,file_name,rec):
        self.file_name = file_name
        self.rec = rec
        self.dirctory = dirctory
        self.temp_path = "pragmataGirl/temp/"
        self.assets_path = "pragmataGirl/assets/"
        self.referans = cv2.imread(self.assets_path + 'referans.png', cv2.IMREAD_UNCHANGED)
        self.end_frame = cv2.imread(self.assets_path + '0744.jpg', cv2.IMREAD_UNCHANGED)
        self.keys = load_interpolated_keys()
        self.video1 = self.assets_path + 'clips/0000-0372.mp4'
        self.video2 = self.assets_path + 'clips/0373-0744.mp4'
        self.clip1_path = "clip1.mp4"
        self.clip2_path = self.temp_path + "_1_" + self.file_name
        self.clip3_path = self.temp_path + "_2_" + self.file_name
        self.clip4_path = self.temp_path + "end_" + self.file_name
        self.state = self.temp_path + self.file_name.replace('mp4','json')
        self.txt_path = self.temp_path + self.file_name.replace('mp4','txt')
        self.audio_path = self.assets_path + "audio.flac"
        self.final_video_path = self.dirctory + self.file_name
        self.type = 'mp4v'
        self.is_canseld = False
        # self.terminate_event = mp.Event()


    def final_scene(self):
        print("start final scene")
        video_writer = cv2.VideoWriter(self.clip4_path, cv2.VideoWriter_fourcc(*self.type), 60, (1920, 1080))
        video_writer.set(cv2.CAP_PROP_BITRATE, 256)

        points = self.keys[744]['points']
        self.end_frame = final_image(self.end_frame, points,self.referans,self.rec)
        for i in range(469):
            v = 1 - (i / 468)
            f = cv2.convertScaleAbs(self.end_frame, alpha=v, beta=0)
            video_writer.write(f)
            with open(self.state, 'r') as file:
                task_state = json.load(file)['state']
            if task_state:
                break
        video_writer.release()

    def delete(self):
        if os.path.exists(self.txt_path):
            os.remove(self.txt_path)
        if os.path.exists(self.clip2_path):
            os.remove(self.clip2_path)
        if os.path.exists(self.clip3_path):
            os.remove(self.clip3_path)
        if os.path.exists(self.clip4_path):
            os.remove(self.clip4_path)
        if os.path.exists(self.state):
            os.remove(self.state)

        # if os.path.exists("temp/temp_rec_" + file_name.replace('mp4','png')):
        #     os.remove("temp/temp_rec_" + file_name.replace('mp4','png'))

    def combine(self):

        file1_exists = os.path.exists(self.clip2_path)
        file2_exists = os.path.exists(self.clip3_path)
        file3_exists = os.path.exists(self.clip4_path)

        if not file1_exists or not file2_exists or not file3_exists:
            return

        with open(self.state, 'r') as file:
            task_state = json.load(file)['state']

        if not task_state:
            files = ["clip1.mp4", "_1_" + self.file_name, "_2_" + self.file_name, "end_" + self.file_name]
            with open(self.txt_path, "w") as file:
                for f in files:
                    file.write("file '" + f + "'\n")

            cmd = f"ffmpeg -f concat -safe 0 -i {self.txt_path} -i {self.audio_path} -c:v copy -c:a aac {self.final_video_path} -loglevel quiet"
            subprocess.call(cmd, shell=True)

            # cmd = f'ffmpeg -i {f} -vf "scale={1440}:{720}" -c:a copy ' + assets
            # subprocess.call(cmd, shell=True)
        else:
            self.is_canseld = True

        self.delete()


    def generate(self):

        print("start")
        total_time_start = time.time()

        data = {"state": False}
        with open(self.state, "w") as file:
            json.dump(data, file)

        self.p1 = mp.Process(target=process,args=(self.video1, self.clip2_path,self.referans,self.rec,self.keys, 0,self.state))
        self.p1.start()
        self.p2 = mp.Process(target=process,args=(self.video2, self.clip3_path,self.referans,self.rec,self.keys, 373,self.state))
        self.p2.start()
        self.final_scene()

        self.p1.join()
        self.p2.join()
        # self.p3.join()

        self.combine()
        print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))

