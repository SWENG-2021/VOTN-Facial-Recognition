### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime
from download import download
from verify import verifyWebhook
import os 
import shutil
import threading
import json
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
        th = threading.Thread(target=downloadImage,args=(asset_id,),daemon=True)
        th.start()
    else:
        print("unverified request")

    return Response(status=200)


def downloadImage(asset_id):
    filename = download(asset_id)
    
    print("Succesfully downloaded: " + filename)
    
    print("Checking that file is an image...")
    
    useless_bit, file_extension = os.path.splitext(filename)
    
    if ((file_extension != ".jpeg") || (file_extension != ".png")):
        return
    else:
        print("File is a compatible image!")
        print("Moving image...")
        shutil.move(filename, os.path.join("https://github.com/SWENG-2021/VOTN-Facial-Recognition/tree/main/unknown_faces", filename))