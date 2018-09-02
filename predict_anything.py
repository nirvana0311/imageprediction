# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 16:14:02 2018

@author: nirva
"""
import os
os.chdir("D:\\study\\IdeaProjects\\Sendtex deep learning\\Keras new\\Keras-Machine-Learning-Deep-Learning-Tutorial-master\\FLASK_SAURABH\\flask_apps")
import numpy as np
import keras
import base64
import io
from keras.preprocessing.image import img_to_array
from PIL import Image
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.models import load_model
from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


def get_model():
    global model
    model = load_model('VGG16_Anything.h5')
    print(" * Model loaded!")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image=image.reshape(1,image.shape[0],image.shape[1],image.shape[2])
    image = preprocess_input(image)

    return image

print(" * Loading Keras model...") 
get_model()

@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))
    
    prediction = model.predict(processed_image)
    label = decode_predictions(prediction)
    response = {
        'prediction': {
            'first': label[0][0][1],
            'second': label[0][1][1]    
        }
    }
    return jsonify(response)


    
    
    
#==============================================================================
# def predict():
#     message = request.get_json(force=True)
#     encoded = message['image']
#     decoded = base64.b64decode(encoded)
#     image = Image.open(io.BytesIO(decoded))
#     processed_image = preprocess_image(image, target_size=(224, 224))
#     prediction = model.predict(processed_image)
#     label = decode_predictions(prediction)
#     response = {
#         'prediction': {
#             'dog': label[0][0][1],
#             'cat': label[0][1][1]
#         }
#     }
#     return jsonify(response)
# 
#     
#     
#==============================================================================
#==============================================================================
# message='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'    
# message='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'
# 
# encoded = message
# 
# decoded = base64.b64decode(encoded)
# image = Image.open(io.BytesIO(decoded))
# processed_image = preprocess_image(image, target_size=(224, 224))
# prediction = model.predict(processed_image)
# label = decode_predictions(prediction)
# response = {
#     'prediction': {
#         'dog': label[0][0][1],
#         'cat': label[0][1][1]
#     }
# }
# 
# label
# #%reset -f
# 
#==============================================================================


