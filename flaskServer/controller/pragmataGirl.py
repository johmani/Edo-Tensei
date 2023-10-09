from flask import request, send_from_directory, abort, jsonify
from pragmataGirl.videoGenerator import VideoGenerator
from flaskServer import app
import numpy as np
import base64
import json
import PIL
import cv2
import io
import os



@app.route('/submit_pragmata_girl', methods=["POST"])
def submit_pragmata_girl():
    data = request.get_json()
    image_data = data.get('image')
    session_number = data.get('sessionNumber')

    mime_type, base64_data = image_data.split(',', 1)
    img_bytes = base64.b64decode(base64_data)
    image = cv2.cvtColor(np.array(PIL.Image.open(io.BytesIO(img_bytes))), cv2.COLOR_RGBA2BGRA)

    process_key = f"{request.access_route[-1]},{session_number}"
    cv2.imwrite(f"{app.root_path}/client/pragmataGirl/image/{process_key}.png", image)

    print(f'Pragmata girl with key {process_key} submitted successfully')
    return jsonify({'message': f'Pragmata girl with key {process_key} submitted successfully'}), 200


@app.route('/pragmata_girl', methods=["POST"])
def pragmata_girl():
    request_data = json.loads(request.data)
    process_key = str(request.access_route[-1]) + ',' + str(request_data.get('sessionNumber'))
    resolution = int(request_data.get('resolution'))

    image = cv2.imread(f"{app.root_path}/client/pragmataGirl/image/{process_key}.png", cv2.IMREAD_UNCHANGED)
    girl = VideoGenerator(f"{app.root_path}/client/pragmataGirl/video/", f'{process_key}.mp4', image,resolution)
    girl.generate()

    if girl.is_canseld:
        message = f'Pragmata girl with key {process_key} closed successfully'
        print(message)
        return jsonify({'message': message}), 200

    message = f'Pragmata girl with key {process_key} generated successfully'
    print(message)
    return jsonify({'message': message}), 200


@app.route('/download_pragmata_girl', methods=["GET"])
def download_pragmata_girl():
    try:
        session_number = request.args.get('sessionNumber')
        process_key = f"{request.access_route[-1]},{session_number}"
        name = f"{process_key}.mp4"
        return send_from_directory(directory=f"{app.root_path}/client/pragmataGirl/video", download_name="pragmata girl.mp4", path=name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/cancel_process', methods=["POST"])
def cancel_process():
    session_number = request.get_json().get('sessionNumber')
    process_key = f"{request.access_route[-1]},{session_number}"

    state_path = f"pragmataGirl/temp/{process_key}.json"

    if os.path.exists(state_path):
        data = {"state": True}
        with open(state_path, "w") as file:
            json.dump(data, file)

        message = f"Process {process_key} canceled successfully"
        print(message)
        return jsonify({"message": f"Process {process_key} canceled successfully"}),200
    else:
        message = f"Process {process_key} closed successfully"
        print(message)
        return jsonify({"message": message}), 200