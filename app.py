from flask import Flask, request, jsonify, request
from flask_marshmallow import Marshmallow
from chatbot import Chatbot
from datetime import datetime

app = Flask(__name__)
chatbot = Chatbot()

# Index placeholder mock page
@app.route("/")
@app.route("/index")
def index():
    return "<h1>HELLO</h1>"

@app.route("/chatbot", methods=["GET"])
def get():
    text = request.args.get("msg")
    response = chatbot.chat(text)
    return jsonify({
        "msg": text,
        "chatbot_response":response,
        "timestamp": str(datetime.now())
        })

if __name__=="__main__":
    app.run()
