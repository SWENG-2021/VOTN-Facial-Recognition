### webhook listener, using flask
import shutil

from flask import Flask, request, Response
from datetime import datetime
from download import download
from verify import verifyWebhook
from metadata import  add_metadata
from new_recognition import loadAllFaces, detectVideoFaces
import os 
import threading

app = Flask(__name__)


@app.route('/addpicture', methods=['POST'])
def addpicture_post():
    print("adding picture initiated")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(request.json)
    headers = request.headers
    timestamp = int(headers["X-Frameio-Request-Timestamp"])
    signature = headers["X-Frameio-Signature"]
    print(timestamp)
    print(signature)
    print(os.getenv("CUSTOM_ACTIONS_SECRET"))
    verified = verifyWebhook("v0", timestamp, request.json, signature, os.getenv("CUSTOM_ACTIONS_SECRET"))
    print(verified)
    if verified:
        asset_id = request.json["resource"]["id"]
        th = threading.Thread(target=downloadImage, args=(asset_id,), daemon=True)
        th.start()
    else:
        print("unverified request")

    return Response(status=200)


def downloadImage(asset_id):
    filename = download(asset_id)

    print("Succesfully downloaded: " + filename)

    print("Checking that file is an image...")

    directory_name, file_extension = os.path.splitext(filename)

    print("file extension: " + file_extension)

    if ((file_extension != ".jpg") and (file_extension != ".png")):
        os.remove(filename)
        print("unsupported image extension")
        print("file removed")
        return
    else:
        print("File is a compatible image!")
        print("Moving image...")
        os.mkdir(os.path.join(os.getcwd(),"known_faces","newly_added_faces",directory_name))
        shutil.move(filename,os.path.join(os.getcwd(),"known_faces","newly_added_faces",directory_name,filename))
        print("Succesfully added image to known faces")

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

    file, file_extension = os.path.splitext(filename)

    print("file extension: " + file_extension)

    if(file_extension != ".mov" and file_extension != ".avi"
            and file_extension != ".m4v" and file_extension != ".mp4"):
        os.remove(filename)
        print("unsupported video format or picture")
        print("file removed")
        return

    print("Succesfully downloaded: " + filename)
    
    print("Starting facial recognition")
    
    description = detect_faces(filename)
    
    print("Sending metadata to frame.io: " + description)
    
    add_metadata(asset_id, description)

    print("Deleted the file: " + filename)
    
    os.remove(filename)


def detect_faces(filename):
    #face recognition
    known_faces, known_names = loadAllFaces()
    faces = detectVideoFaces(filename, known_faces, known_names, debug_mode=False)

    #format into a descrption
    
    desc = ""
    
    for face in faces:
        desc = desc + str(face) +": "
        for elem in faces[face]:
            desc = desc + str(elem) +" "
        desc = desc + "\n"
        
    return desc
