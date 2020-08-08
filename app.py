from flask import Flask, request, jsonify, request
from flask_marshmallow import Marshmallow
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

# Index placeholder mock page
@app.route("/")
@app.route("/index")
def index():
    return "<h1>HELLO</h1>"

@app.route("/rest", methods=["GET"])
def get():
    text = request.args.get("text")
    response = chatbot.chat(text)
    return jsonify({"msg":response})

if __name__=="__main__":
    app.run()
