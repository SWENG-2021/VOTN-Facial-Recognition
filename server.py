### webhook listener, using flask
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/',methods=['POST'])
def webhook_post():
    print("POST")
    print(request.json)
    return Response(200)

@app.route('/',methods=['GET'])
def webhook_get():
    print("GET")
    print(request.json)
    return Response(200)

