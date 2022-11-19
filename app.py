from flask import Flask, render_template, request, redirect, url_for
from os.path import join, dirname, realpath
from glob import glob
import numpy as np
import os
import cv2, imutils
import tensorflow as tf

VIDEO = join(dirname(realpath(__file__)), "static/uploads/videos")
FRAMES = join(dirname(realpath(__file__)), "static/frames")
RESIZED = join(dirname(realpath(__file__)), "static/resized")

app = Flask(__name__, template_folder="template")
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        os.makedirs(VIDEO)
        if request.files:
            video = request.files["video"]
            video.save(os.path.join(VIDEO, video.filename))
            os.makedirs(FRAMES)
            return redirect(url_for("frames"))
    return render_template("index.html")

@app.route("/frames")
def frames():
    os.makedirs(RESIZED)
    def save_frame(video_path, gap):
        images_array = []
        name = video_path.split("\\")[1].split(".")[0]
        cap = cv2.VideoCapture(video_path)
        index = 0

        while True:
            ret, frame = cap.read()
            if ret == False:
                cap.release()
                break
            if frame is None:
                break
            else:
                if index == 0:
                    images_array.append(frame)
                    cv2.imwrite(f"static/frames/{index}.jpeg", frame)
                else:
                    if index % gap == 0:
                        images_array.append(frame)
                        cv2.imwrite(f"static/frames/{index}.jpeg", frame)
            index += 1
        return np.array(images_array)

    video_paths = glob("static/uploads/videos/*")
    for path in video_paths:
        array_of_images = save_frame(path, gap=10)
        return redirect(url_for("resize"))

    return render_template("frames.html")

@app.route("/resize")
def resize():  
    def resize_frames():
        frame_paths = glob(f"static/frames/*.jpeg")
        index = 0
        width, height = (299, 299)

        for frame in frame_paths:
            image = cv2.imread(frame)
            image_resized = cv2.resize(image, (299, 299))
            cv2.imwrite("static/resized/%i.jpeg"%index, image_resized)
            
            index += 1   
    resize_frames()
    images = os.listdir(FRAMES)
    images = [ "frames/" + image for image in images]
    videos = os.listdir(VIDEO)
    videos = [ "uploads/videos/" + video for video in videos]

    return render_template("index.html", images=images, video=videos[0], code=True)

@app.route("/delete")
def delete():
    if os.path.exists(VIDEO):
        os.rmdir(VIDEO)

    if os.path.exists(FRAMES):
        os.rmdir(FRAMES)
    
    if os.path.exists(RESIZED):
        os.rmdir(RESIZED)

    return redirect(url_for("index"))

@app.route("/predict", methods=["POST","GET"])
def predict():
    def fetch_frames():
        frame_paths = glob(f"static/resized/*.jpeg")
        query_frames_array = []

        for frame in frame_paths:
            image = cv2.imread(frame)
            query_frames_array.append(image)
        return np.array(query_frames_array)

    query_frames_array = fetch_frames()
    video_frame_classifier = tf.keras.models.load_model("inception_saved")
    query_results = video_frame_classifier.predict(query_frames_array)
    decoded_query_results = tf.keras.applications.inception_v3.decode_predictions(query_results, top=5)

    def showResults(decoded_response):
        search_query_value = request.form["search_query"]
        print("search_query_value", search_query_value)
        for i in range(len(decoded_response)):
            class_tupple = decoded_response[i]
            _id, frame_class, frame_prob = class_tupple[0]
            image_index = i
            if search_query_value == "":
                pass
            elif search_query_value == frame_class:
                image_index = i
                break
        return i*10, frame_class
    image_index, frame_class = showResults(decoded_query_results)
    images = os.listdir(FRAMES)
    images = [ "frames/" + image for image in images]
    videos = os.listdir(VIDEO)
    videos = [ "uploads/videos/" + video for video in videos]
    return render_template("index.html",index=image_index, class_name=frame_class, images=images, video=videos[0], code=True)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    with make_server("", 5000, app) as server:
        print("serving on port 5000...")
        server.serve_forever()
    
    