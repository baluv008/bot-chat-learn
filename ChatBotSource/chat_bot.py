"""
Module to run the main algorithm
"""
from urllib import response

from flask import session
from BotPredictor import get_features
from web_scraper import *
import numpy as np
import pickle
responses = pickle.load(open("responses.pk1", "rb"))

class ChatBot:

    def __init__(self,message=None,is_basic_message=False):
        self.incoming_message = message.lower()

    def get_response(self):
        print(session)
        response = ""
        q_type,features = get_features(self.incoming_message)
        print(q_type,features)
        if features == {} and q_type not in ["ticket_price"]:
            response = self.__checkfor_greetings__(q_type)
        else:
            session["source"] = features.get("source", "")
            session["destination"] = features.get("destination", "")

            response = self.__get_question_answer__(q_type,features)

        return response
    def __checkfor_greetings__(self,q_type):
        global responses
        return np.random.choice(responses[q_type])

   
    def __get_question_answer__(self,*args):
        q_type = args[0]
        features = args[1]#
        output = "Invalid Question"
        destination = ""
        source = ""
        if q_type == "timing_from_to_after":
            source = features.get("source",None)
            destination = features.get("destination",None)
            travel_time = features.get("travel_time","0000")
            travel_date = features.get("travel_date","today")
            if None not in [source, destination]:
                d,c,output = get_train_from_to(source,destination,travel_date,travel_time)
                print(c,output)
                session["duration"] = d
                print(session["stations"])
        elif q_type == "ticket_price":
            output = session["price"]
        elif q_type == "stops_between":

            travel_time = features.get("travel_time", "0000")
            travel_date = features.get("travel_date", "today")
            source = session["source"]
            destination = session["destination"]

            get_train_from_to(source, destination, travel_date, travel_time)
            stations = []
            if "stations" in session and (None not in[destination,source] and (destination == session["destination"] and source == session["source"]) ):

                stations = session["stations"]
            else:
                if source is None:
                    source = session["source"]
                if destination is None:
                    destination = session["destination"]

                print(get_train_from_to(source,destination,travel_date,travel_time))
                stations = session["stations"]
            output = "%s<br>%s" %("The stations are","<br>".join(stations))

        return output


    
