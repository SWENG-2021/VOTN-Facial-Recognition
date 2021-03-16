### webhook listener, using flask
from flask import Flask, request, Response
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook_post():
    print("POST")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(request.json)
    return Response(status=200)

@app.route('/webhook',methods=['GET'])
def webhook_get():
    print("GET")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(request.json)
    return Response(status=200)

