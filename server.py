### webhook listener, using flask
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    print(request.json)
    if request.method == 'POST':
        return Response(status=200)
    else:
        return Response(status=400)

if __name__ == '__main__':
    app.run(port=5000)
