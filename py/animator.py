import json

import numpy as np
import pandas as pd


def linear_interpolation(x1, y1, x2, y2, t):
    interpolated_x = (1 - t) * x1 + t * x2
    interpolated_y = (1 - t) * y1 + t * y2
    return interpolated_x, interpolated_y


def interpolation_point(point1, point2, frame_count):
    frame_count = abs(frame_count)
    interpolated_frames = []
    for frame in range(frame_count):
        t = frame / (frame_count - 1)  # Calculate t for the current frame
        interpolated_x, interpolated_y = linear_interpolation(point1[0], point1[1], point2[0], point2[1], t)
        interpolated_frames.append((round(interpolated_x), round(interpolated_y)))
    return np.array(interpolated_frames)


def interpolate_rectangle(list1, list2):
    req1 = np.array(list1['points'])
    req2 = np.array(list2['points'])

    from_frame = list1['image_name']
    to_frame = list2['image_name']
    images_name = np.arange(from_frame, to_frame + 1, 1)
    frame_count = len(images_name)
    sq = []
    for p1, p2 in zip(req1, req2):
        inter_point = interpolation_point(p1, p2, frame_count)
        sq.append(inter_point)

    sq = np.array(sq).transpose(1, 0, 2)
    return sq, images_name


def load_keys():
    with open("res/keys.json", "r") as infile:
        js = json.load(infile)
    results_js = sorted(js, key=lambda x: x['image_name'])

    return results_js

def load_interpolated_keys():
    js = load_keys()
    data = []
    for i in range(len(js)):
        if i + 1 < len(js):
            rectangle1 = js[i]
            rectangle2 = js[i + 1]

            points, images_names = interpolate_rectangle(rectangle1, rectangle2)
            for r, name in zip(points, images_names):
                data.append({'image_name': name, 'points': r})

    df = pd.DataFrame(data).drop_duplicates(subset=['image_name'])
    js = json.loads(df.to_json(orient='records'))

    return js


def get_rectangle(image_name, shift = 0):
    js = load_keys()
    data = []
    for i in range(len(js)):
        if i + 1 < len(js):
            rectangle1 = js[i]
            rectangle2 = js[i + 1]

            points, images_names = interpolate_rectangle(rectangle1, rectangle2)
            for r, name in zip(points, images_names):
                data.append({'image_name': name, 'points': r})

    df = pd.DataFrame(data).drop_duplicates(subset=['image_name'])
    image_name = image_name + shift
    if len(df[df['image_name'] == image_name]) > 0:
        return df[df['image_name'] == image_name]['points'].values[0]
    else:
        return np.array([[0, 800], [1920, 900], [1920, 1080], [0, 1080]])



def get_nearest_key(image_name):
    js = load_keys()
    left_records = [record for record in js if record["image_name"] < image_name]
    right_records = [record for record in js if record["image_name"] > image_name]
    return np.array(left_records[len(left_records)-1]['points']),np.array(right_records[0]['points'])

