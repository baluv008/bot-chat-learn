import pickle
import nltk
from nltk.stem import WordNetLemmatizer as Lemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def clean_sentance(sentance):

    lemmatizer = Lemmatizer()
    stop_words = set(stopwords.words("english"))
    key_words = nltk.word_tokenize(sentance)
    key_words = [lemmatizer.lemmatize(word.lower()) for word in key_words]
    return " ".join(key_words)
def tranform_sentance(sentance, corpuses):
    vectorizer = CountVectorizer()
    sentance = [clean_sentance(s) for s in sentance]
    transformed_sentance = vectorizer.fit(corpuses).transform(sentance)
    return transformed_sentance