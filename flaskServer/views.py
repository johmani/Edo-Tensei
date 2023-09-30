import json
import cv2
import numpy as np
from flask import render_template, request, redirect, send_from_directory, abort, make_response
from PIL.Image import open
import base64
import io
import datetime
import  multiprocessing as mp
from pragmataGirl.py.pragmataGirl import gene
from flaskServer import app



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pragmataGirl')
def pragmata_girl_page():
    return render_template('pragmataGirl.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/pragmata_girl', methods=["POST"])
def pragmata_girl():

    request_data = json.loads(request.data)
    image_data = request_data.get('image')

    mime_type, base64_data = image_data.split(',', 1)
    img_bytes = base64.b64decode(base64_data)
    img = open(io.BytesIO(img_bytes))
    image = np.array(img)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    file_name = f'{request.access_route[-1]},{formatted_time}'

    # cv2.imwrite(f'temp/temp_rec_{request.remote_addr},{formatted_time}.png', image)

    p = mp.Process(target=gene,args=(image,file_name + '.mp4'))
    p.start()
    p.join()

    cook = make_response("DONE", 200)
    cook.set_cookie("pragmata_girl_download", str(file_name))

    return cook

# @app.route('/pragmata_girl_state')
# def pragmata_girl_state():
#     file_name = request.cookies.get("pragmata_girl_download")
#     rec = cv2.imread(f'temp/temp_rec_{file_name}.png', cv2.IMREAD_UNCHANGED)
#     file_name = file_name + '.mp4'
#     def generate_event(file_name,rec):
#         print("start")
#         print(file_name,rec.shape)
#         yield f"data: {0}\n\n"
#
#         total_time_start = time.time()
#
#         p1 = mp.Process(target=process, args=('assets/p2/0000-0372.mp4', "temp/_1_" + file_name, 0, rec))
#         p2 = mp.Process(target=process, args=('assets/p2/0373-0744.mp4', "temp/_2_" + file_name, 373, rec))
#
#         p1.start()
#         yield f"data: {5}\n\n"
#         p2.start()
#         yield f"data: {10}\n\n"
#
#         final_scene(file_name, rec)
#
#         yield f"data: {30}\n\n"
#
#         p1.join()
#         yield f"data: {60}\n\n"
#         p2.join()
#         yield f"data: {95}\n\n"
#
#         combine(file_name)
#         yield f"data: {100}\n\n"
#
#         print('total_time_start : ', "%s seconds" % (time.time() - total_time_start))
#
#     return Response(generate_event(file_name,rec),content_type='text/event-stream')

@app.route('/download_pragmata_girl', methods=["GET"])
def download_pragmata_girl():

    try:
        name = request.cookies.get("pragmata_girl_download") + '.mp4'
        print(name)
        return send_from_directory(directory=app.config['VIDEO_DIR'], download_name="pragmata girl.mp4", path=name,as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/delete_cookie', methods=["GET"])
def delete_cookie():
    cook = make_response("DONE", 200)
    cook.set_cookie("pragmata_girl_download", "N")
    return cook



