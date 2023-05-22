import spacy
import string
import time
#from geotext import GeoText

import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup
import unicodedata
import dateutil.parser as dparser
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from dbconn import *


nlp = spacy.load("fr_core_news_sm", parse=True, tag=True, entity=True)

#text = u'Cest la fete le match de foot au Stade de France hihihi le 27/03/12 nul giroux la girouette'
#text = u'Tous les films de Ghibli chez Netflix'

def token(sentence): #Tokenize et retourne les labels
    doc = nlp(sentence)
    return [(X.text, X.label_) for X in doc.ents]

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def normalize_corpus(text):
    normalize_text = remove_accented_chars(text)
    normalize_text = remove_special_characters(normalize_text)
    normalize_text = lemmatize_text(normalize_text)
    return normalize_text

def remove_stopwords(text):
    stopword_list = stopwords.words('french')
    tokens = word_tokenize(text)
    tokensWithoutPunc = [word for word in tokens if word not in stopword_list]
    filtered_text = ' '.join(tokensWithoutPunc)
    return filtered_text



def create_vector(features,tokens):
    v = [0 for i in range(0,len(features))]
    for i in range(0,len(features)):
        if features[i] in tokens :
            #if features[i] == 
            v[i]=1
    return v
        
def vectorization(f) :
    #Changer pour vous:Hp6ZTa7
    #connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient("mongodb+srv://martin:Hp6ZTa7@tweets-yzhnw.mongodb.net/test?retryWrites=true&w=majority")
    db=client.admin
    mydb = client["Tweet"]
    mycol = mydb["tweets"]
    i = 0
    vecteur_count = 0

    ## ATTENTION ##
    deleteAllVectors()
    ##           ##

    for t in mycol.find({}):
        
        normalize_text = normalize_corpus(t.get('text'))
        
        final_text = remove_stopwords(normalize_text)
        #print(final_text)

        #creation du vecteur
        v = create_vector(f,final_text.split(" "))
        #print(v)

    ##################################DEBUG AND INSERT###########################################################################
        #c est juste pour voir si ya des vecteurs avec des 1 => oui
        if sum(v) >=1 :
            insert_vector(v,t.get('text'),t.get('tweet_id'),t.get('date'))
            vecteur_count +=1
        i+=1
        print("nb possibles Event : ",vecteur_count, "/", i,time.perf_counter())


#on lemmatize les features pr la proprete
features = "sport foot stade football athletisme basketball natation cyclisme golf handball equitation judo karate marathon rugby ski taekwondo volleyball superbowl match coupe championnat attentat tremblement concert exposition explosion festival terroriste election fete cirque gala oscar cesar congre forum ceremoni convention spectacle theatr politique trianon vote election accident mort sortie album cinema film coronaviru viru maladie epidemie pandemie nouveau solde carnaval france europe monde national regionnal zenith olympia bataclan hippodrome cinema"
f = lemmatize_text(features).split(" ")

vectorization(f)

#test API pour la localisation mais osef

#places = GeoText("text")
#print(places.cities)
