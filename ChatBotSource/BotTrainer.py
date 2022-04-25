from json import load as jsload

import numpy
import numpy as np
import random
import pickle
import nltk
from nltk.stem import WordNetLemmatizer as Lemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import  confusion_matrix
# from tensorflow.keras.models import  Sequential
# from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD
stop_words = set(stopwords.words("english"))
data = []

with open('intentions.json') as file:  # intents file holds the responses and lables for bot training
    data = jsload(file)

vectorizer = CountVectorizer()
lemmatizer = Lemmatizer()
vetrozed_array = []
key_words = []
classifications = []
docs = []
exclussions = ["?","!","."]
corpuses = []
classes = []
types_responses = {}
for intentions in data["intentions"]:
    types_responses[intentions["type"]] = intentions["outgoing"]
    for incoming in intentions["incoming"]:
        words = nltk.word_tokenize(incoming)

        corpuses.append(incoming.lower())
        classes.append(intentions["type"])
        key_words.extend(words)

        docs.append((words, intentions["type"]))
        if intentions["type"] not in classifications:
            classifications.append(intentions["type"])


key_words = [lemmatizer.lemmatize(word) for word in key_words if word not in exclussions and word not in stop_words]
key_words =  sorted(set(key_words))

print(key_words)


counts = vectorizer.fit(corpuses)

training = counts.transform(corpuses)

tf_training = TfidfTransformer().fit(training).transform(training)

outputs = vectorizer.fit(classifications).vocabulary_

output_types = [outputs[clas] for clas in classes]

model = MultinomialNB().fit(training,output_types)

predictions = model.predict(training)

pickle.dump(corpuses, open("corpuses.pk1","wb"))

pickle.dump(outputs, open("types.pk1","wb"))
pickle.dump(types_responses,open("responses.pk1","wb"))
pickle.dump(model, open("bot_model.model","wb"))






