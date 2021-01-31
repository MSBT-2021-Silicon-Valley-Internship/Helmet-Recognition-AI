from flask import Flask, flash, request, redirect, url_for, session, jsonify
from db_connection import insert_helmet
from syndicai import PythonPredictor
from werkzeug.utils import secure_filename
import logging
import datetime

from flask_cors import CORS, cross_origin

import os

app = Flask(__name__)
logger = logging.getLogger('HELLO WORLD')

@app.route('/')
def index():
    return "Helmet Detection", 200

@app.route('/images', methods=['POST'])
def process():
    fileUpload()
    updatedb()
    predict()


def predict():
    """ Return JSON serializable output from the model """
    payload = request.args
    detector = PythonPredictor("")
    return detector.predict(payload)
 
def updatedb():
    pass

UPLOAD_FOLDER = '/usr/src/app'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'imgfolder')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")

    #SAVE NAME : DATE
    now = datetime.datetime.now() # 2015-04-19 12:11:32.669083
    nowDate = now.strftime('%Y-%m-%d')# 2015-04-19
    nowTime = now.strftime('%H:%M:%S')# 12:11:32
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')# 2015-04-19 12:11:32

    #attaching date to name
    file = request.files['file']
    print(file)
    file.save(file)

    filename = "".join([nowDatetime, secure_filename(file.filename)])
    print(filename)
    file.save(filename)

    destination="/".join([target, filename])
    print(destination)
    file.save(destination)
    #session['uploadFilePath']=filename
    session['uploadFilePath']=destination
    response={'response': 'hello', 'fileurl': destination}
    #Json 형태로
    return jsonify(response)