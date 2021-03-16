### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime
from download import download
from verify import verifyWebhook
from os import getenv
from os import system
from metadata import  add_metadata
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
    print(getenv("SECRET"))
    verified = verifyWebhook("v0",timestamp,request.json,signature,getenv("SECRET"))
    print(verified)
    if verified:
        asset_id = request.json["resource"]["id"]
        filename = download(asset_id)
        system("./deleteFile "+filename)
        ##
        ###face recognition here
        add_metadata(asset_id,"TEST DESCRIPTION\n AAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAA")
    else:
        print("unverified request")

    return Response(status=200)


