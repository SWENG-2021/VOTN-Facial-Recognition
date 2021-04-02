### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime
from download import download
from verify import verifyWebhook
from metadata import  add_metadata
from new_recognition import loadAllFaces, detectVideoFaces
import os 
import threading
app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook_post():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(request.json)
    headers = request.headers
    timestamp = int(headers["X-Frameio-Request-Timestamp"])
    signature = headers["X-Frameio-Signature"]
    print(timestamp)
    print(signature)
    print(os.getenv("SECRET"))
    verified = verifyWebhook("v0",timestamp,request.json,signature,os.getenv("SECRET"))
    print(verified)
    if verified:
        asset_id = request.json["resource"]["id"]
        th = threading.Thread(target=processVideo,args=(asset_id,),daemon=True)
        th.start()
    else:
        print("unverified request")

    return Response(status=200)


def processVideo(asset_id):
    filename = download(asset_id)

    ###face recognition here
    description = detect_faces(filename)
    add_metadata(asset_id, description)

    ###deletion
    os.remove(filename)


def detect_faces(filename):
    #face recognition
    known_faces, known_names = loadAllFaces()
    faces = detectVideoFaces(filename, known_faces, known_names, debug_mode=False)

    #format into a descrption
    desc = ""
    for face in faces:
        desc += face+"\n"

    return desc