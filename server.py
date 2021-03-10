### webhook listener, using flask
from flask import Flask, request, Response
from flask_ngrok import run_with_ngrok 

app = Flask(__name__)
run_with_ngrok(app) 


@app.route('/',methods=['POST'])
def webhook_post():
    print("POST")
    print(request.json)
    return Response(status=200)

@app.route('/',methods=['GET'])
def webhook_get():
    print("GET")
    print(request.json)
    return Response(status=200)

if __name__ == "__main__": 
  app.run()
