
from flask import Flask, render_template, request,session
from flask_session import Session
import json
import time
from datetime import timedelta

from chat_bot import ChatBot

chatbot_app = Flask(__name__, template_folder="templates",static_folder = "static")
chatbot_app.config["SESSION_PERMANENT"] = True
chatbot_app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
chatbot_app.config["SESSION_TYPE"] = "filesystem"
Session(chatbot_app)

@chatbot_app.route("/")
def homepage():
    return render_template("index.html")
@chatbot_app.route("/new")
def testPage():
    return render_template("index2.html")
@chatbot_app.route("/chat", methods=[ 'POST'])
def recieve_chat():
    data=request.form['chat_msg']
    print(data)
    Bot = ChatBot(data,False) 
    result = Bot.get_response()
    return result

    
if __name__ == "__main__":
    chatbot_app.run(host="0.0.0.0",debug=True)
    # chatbot_app.run( debug=True)
