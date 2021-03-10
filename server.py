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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
