import json
import cv2
import numpy as np
from flask import render_template, request, Response, redirect, send_from_directory, abort, session,make_response
from PIL.Image import open
import base64
import io
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import datetime
import re
import  multiprocessing as mp
from py.animator import load_interpolated_keys
from py.generate_v2 import gene
import time



from flaskServer import app




@app.route('/sign-up',methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        print(request.form)
        redirect(request.url)
    return render_template('test.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pragmataGirl')
def pragmata_girl_page():
    return render_template('pragmataGirl.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/CCC')
def CCC():
    ccc = make_response("Cookies", 200)
    ccc.set_cookie("V1_", "name1")
    return ccc

@app.route('/pragmata_girl', methods=["POST"])
def pragmata_girl():
    # global image
    request_data = json.loads(request.data)
    image_data = request_data.get('image')
    # file_name = request_data.get('file_name')

    mime_type, base64_data = image_data.split(',', 1)
    img_bytes = base64.b64decode(base64_data)
    img = open(io.BytesIO(img_bytes))
    image = np.array(img)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f")
    full_name = request.remote_addr + "," + formatted_time



    # res = gene(image,full_name+'.mp4')
    p = mp.Process(target=gene,args=(image,full_name+'.mp4'))
    p.start()
    p.join()

    cook = make_response("DONE", 200)
    cook.set_cookie("pragmata_girl_download", str(full_name))


    return cook

# def generate_event():
#
#     yield f"data: {0}\n\n"
#     total_time_start = time.time()
#     edit_start_time = time.time()
#     keys = load_interpolated_keys()
#     referans = cv2.imread('res/referans11.png', cv2.IMREAD_UNCHANGED)
#     video_capture = cv2.VideoCapture('res/cuted0000-0744.mp4')
#
#     new_clip = []
#     image_name = 0
#     while video_capture.isOpened():
#         ret, frame = video_capture.read()
#         if not ret:
#             break
#         points = keys[image_name]['points']
#         frame = final_image(frame, points, referans, image)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
#         new_clip.append(frame)
#         image_name = image_name + 1
#         r = int((image_name / 745 / 2) * 100)
#         yield f"data: {r}\n\n"
#     video_capture.release()
#     print('edit : ', "%s seconds" % (time.time() - edit_start_time))
#
#     generate_video_start = time.time()
#
#     new_clip = ImageSequenceClip(new_clip, fps=60)
#     new_clip = new_clip.subclip(0, 20.9)
#     new_clip = new_clip.fadeout(7)
#     audio = AudioFileClip("res/a1.flac")
#     new_clip = new_clip.set_audio(audio)
#
#     clip1 = VideoFileClip("res/clip1.mp4")
#     final_video = concatenate_videoclips([clip1, new_clip])
#
#
#     final_video.write_videofile(app.config['VIDEO_DIR']+'/nameplate_girl.mp4')
#
#     clip1.close()
#     new_clip.close()
#     final_video.close()
#
#     print('generate video : ', "%s seconds" % (time.time() - generate_video_start))
#     print('total time : ', "%s seconds" % (time.time() - total_time_start))
#     yield f"data: {100}\n\n"


# @app.route('/pragmata_girl_state')
# def pragmata_girl_state():
#     return Response(generate_event(),content_type='text/event-stream')



@app.route('/download_pragmata_girl', methods=["GET"])
def download_pragmata_girl():

    try:
        name = request.cookies.get("pragmata_girl_download")
        file_name = name + ".mp4"
        print(file_name)
        return send_from_directory(directory=app.config['VIDEO_DIR'], download_name="pragmata girl.mp4", path=file_name,as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/delete_cookie', methods=["GET"])
def delete_cookie():
    cook = make_response("DONE", 200)
    cook.set_cookie("pragmata_girl_download", "N")
    return cook



