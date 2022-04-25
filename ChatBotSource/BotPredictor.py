import pickle
from common_functions import *
from nltk import word_tokenize
from flask import session
from datetime import  datetime
import dateutil.parser as dparser
corpuses = pickle.load(open("corpuses.pk1","rb"))
model = pickle.load(open("bot_model.model","rb"))
types = pickle.load(open("types.pk1","rb"))
inverted_types = {v:k for k,v in types.items()}

def predict_type(incoming):
    ts = tranform_sentance([incoming], corpuses)
    return inverted_types[model.predict(ts)[0]]
def get_features(question):
    q_type = predict_type(question)

    source = None
    destination = None
    travel_date = "today"

    travel_time = "%s%s"%(datetime.now().hour,datetime.now().minute)
    live = ""
    key_words = word_tokenize(question)
    words = {inx:value for inx, value in enumerate(key_words)}
    features = {}
    print(key_words)
    if q_type in ["timing_from_to_after","stops_between"]:
        features["travel_time"] = travel_time
        features["travel_date"] = travel_date
        if "from" in key_words:
            source = words.get(key_words.index("from")+1,None)
            features["source"] = source
            live = source

        if "to" in key_words:
            destination = words.get(key_words.index("to") + 1, None)
            features["destination"] = destination
            live = destination
        if "between" in key_words:
            source = words.get(key_words.index("between") + 1, None)
            features["source"] = source
        if "and" in key_words:
            destination = words.get(key_words.index("and") + 1, None)
            features["destination"] = destination
        if source is None and destination is None:
            source = session["source"]
            destination = session["destination"]
            features["destination"] = destination
            features["source"] = source
        features["live"] = live
        if features.get("source",None) is not None:
            session["source"] = features["source"]
        if features.get("destination",None) is not  None:
            session["destination"] = features["destination"]
        try:
            date_time = dparser.parse(question, fuzzy=True)
            date = date_time.date().strftime("%d%m%Y")
            time = date_time.time().strftime("%H%M")
            features["travel_date"] = date
            features["travel_time"] = time
        except:
            pass


    return q_type,features




# q_type,features = get_features("What are the station in between london and norwich".lower())
#
# print(q_type)
# print(features)
# q_type,features = get_features("How many stops".lower())
# print(q_type)
# print(features)