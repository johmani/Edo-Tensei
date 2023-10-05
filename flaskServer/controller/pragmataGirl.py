from flask import request, send_from_directory, abort, jsonify
from pragmataGirl.videoGenerator import VideoGenerator
from flaskServer import app
from PIL.Image import open
import numpy as np
import base64
import json
import cv2
import io


active_processes = {}


@app.route('/submit_pragmata_girl', methods=["POST"])
def submit_pragmata_girl():
    try:
        data = request.get_json()
        image_data = data.get('image')
        session_number = data.get('sessionNumber')

        mime_type, base64_data = image_data.split(',', 1)
        img_bytes = base64.b64decode(base64_data)
        image = cv2.cvtColor(np.array(open(io.BytesIO(img_bytes))), cv2.COLOR_RGBA2BGRA)

        process_key = f"{request.access_route[-1]},{session_number}"

        girl = VideoGenerator(app.config['VIDEO_DIR'] + '/',f"{process_key}.mp4", image)
        active_processes[process_key] = girl

        print(f'Pragmata girl with key {process_key} submitted successfully')
        return jsonify({'message': f'Pragmata girl with key {process_key} submitted successfully'}),200

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/pragmata_girl', methods=["POST"])
def pragmata_girl():
    request_data = json.loads(request.data)
    process_key = str(request.access_route[-1]) + ',' + str(request_data.get('sessionNumber'))
    girl = active_processes[process_key]
    girl.generate()

    if active_processes[process_key] != None:
        del active_processes[process_key]

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
        name = f"{str(request.access_route[-1])},{str(session_number)}.mp4"
        return send_from_directory(directory=app.config['VIDEO_DIR'], download_name="pragmata girl.mp4", path=name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/cancel_process', methods=["POST"])
def cancel_process():
    try:
        session_number = request.get_json().get('sessionNumber')
        process_key = f'{request.remote_addr},{str(session_number)}'

        if process_key in active_processes:
            active_processes[process_key].cansel()
            return jsonify({"message": f"Process {process_key} canceled successfully"})
        else:
            print(f"Process {process_key} closed successfully")
            return jsonify({"message": f"Process {process_key} closed successfully"}), 200

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}),500