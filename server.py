### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime
from download import download
app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook_post():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(request.json)

    asset_id = request.json["resource"]["id"]
    download(asset_id)



    return Response(status=200)


