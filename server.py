### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime
from download import download
from verify import verifyWebhook
from os import getenv
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
    asset_id = request.json["resource"]["id"]
    download(asset_id)
    return Response(status=200)


