from flask import Flask, request, jsonify, flash
import os
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from Preprocessing import Preprocessing

app = Flask(__name__)

UPLOAD_FOLDER = 'img'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_dark(image, threshold=100):
    return np.mean(image) < threshold

@app.route('/picture',methods=['POST'])
def post_picture():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "File Failed"
        file = request.files['file']
        architecture = request.form['architecture']
        if file.filename == '':
            flash('No selected file')
            return "File Failed"
        if file:
            try:
                img_stream = file.stream
                img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
                img_opencv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                labels = ["Bantal Kepala","Bola","Dompet","Garpu","Gelas Mug",
                    "Gunting","Headphones","Jaket","Jam Alarm","Kaos",
                    "Kipas Angin","Kursi","Meja","Penghapus","Pisau",
                    "Sendal Jepit","Sendok","Sepatu","Sikat Gigi","Teko Teh"]
                dark_detector = "Gambar Terang"
                if(is_dark(img_opencv)):
                    dark_detector = "Gambar Gelap"
                model = tf.keras.models.load_model("Model/resnet18.h5")
                if(architecture == "MobileNetV1"):
                    model = tf.keras.models.load_model("Model/mobilenetv1.h5")
                resize = Preprocessing.resize(img_opencv)
                resize = np.expand_dims(resize,axis=0)

                predictions = model.predict(resize)
                predicted_label = labels[np.argmax(predictions)]
                prediction_probability = np.max(predictions) * 100
                result = {
                    'status':"success",
                    'data':{
                        'architecture':architecture,
                        'dark_detector':dark_detector,
                        'predicted_label':predicted_label,
                        'prediction_probability':prediction_probability
                    }
                }
                return jsonify(result),201
            except:
                result = {
                    'status':"error",
                    'message':"Terdapat kesalahan pada sistem"
                }
                return jsonify(result),400

if __name__ == '__main__':
    app.run(debug=True)