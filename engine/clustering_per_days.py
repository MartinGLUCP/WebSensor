import collections
import os
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MeanShift, DBSCAN,estimate_bandwidth

import logging
from optparse import OptionParser
import sys

import numpy as np
from pymongo import MongoClient

from testNLP import *
from connectMongo import *

import time

from pymongo import MongoClient

from dbController import insertEvent

from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop

from scratchdbscan import MyDBSCAN

final_stopwords_list = list(fr_stop) + list(en_stop)

"""
serveur = 'local' #'online'

if serveur == 'online':
    # MongoDB connection info
    hostname = 'mongodb-[projetagp].alwaysdata.net'
    port = 27017
    username = 'projetagp'
    password = 'projet2020'
    databaseName = 'projetagp_mongo'
else:
    hostname = 'localhost'
    port = 27017
    username = 'admin'
    password = 'admin'
    databaseName = 'webSensor'

client = MongoClient('mongodb://localhost:27017/')
db = client.webSensor
"""

def subject(sentence,features):
        subject =""
        tokens = normalize_corpus(sentence)
        for i in range(len(features)):
                if features[i] in tokens :
                        subject += features[i] + " "
        return subject

def getMaxFollowerTweet(tweet_id,followers_count) :
    idMax = followers_count.index(max(followers_count))
    return tweet_id[idMax]


collectionsMongo = list(db.list_collection_names())
collectionsMongo = sorted(collectionsMongo)

for currentCollection in collectionsMongo:
        print("Start with ",currentCollection)
        _complete_dataset = selectAll(currentCollection)

        dataset = _complete_dataset['text']

        date = list(set(_complete_dataset['date']))
        
        nb_user = len(list(set(_complete_dataset['user_id'])))

        start_time = time.time()

        max_features = len(dataset)*0.01
        max_min_samples = len(dataset)*0.001
        #int(max_features), stop_words=final_stopwords_list
        tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,max_df=0.3, stop_words=final_stopwords_list,ngram_range=(1,2),max_features=int(max_features))
        
        #tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize_corpus,max_df=0.7, stop_words=final_stopwords_list,ngram_range=(1,3),binary= True, norm = None, use_idf = False,max_features=int(max_features))
        X = tfidf_vectorizer.fit_transform(dataset).toarray()

        vocabulary = tfidf_vectorizer.get_feature_names()

        print(vocabulary)
        print(" ")
        print(date,"--- Clustering",len(dataset),"starting in %s seconds ---" % (time.time() - start_time))
        ml = DBSCAN(eps=0.5, min_samples=max_min_samples,n_jobs=-1)
        print("->")
        ml.fit(X)
        print(date,"--- Clustering finish in %s seconds ---" % (time.time() - start_time))
        n_clusters_ = len(set(ml.labels_)) - (1 if -1 in np.unique(ml.labels_) else 0)
        n_noise_ = list(ml.labels_).count(-1)
        
        _cluster_info = {}

        for i in range(n_clusters_):
            _cluster_info['cluster'+str(i)+'_tweets']=[]
            _cluster_info['cluster'+str(i)+'_followers_count']=[]
            _cluster_info['cluster'+str(i)+'_user_id']=[]

        clusters = collections.defaultdict(list)
        for i, label in enumerate(ml.labels_):
            clusters[label].append(i)


        total_data = {key :0 for key in range(n_clusters_)}
        total_feature = {}
        pourcentage = {key :[] for key in range(n_clusters_) }

        _cluster_info['n_clusters']=n_clusters_
        
        clusters = dict(clusters)
        for cluster in range(n_clusters_):
        
            for i,sentence in enumerate(clusters[cluster]):

                _cluster_info['cluster'+str(cluster)+'_tweets'].append(_complete_dataset['tweet_id'][dataset.index(dataset[sentence])])
                _cluster_info['cluster'+str(cluster)+'_followers_count'].append(_complete_dataset['followers_count'][dataset.index(dataset[sentence])])
                _cluster_info['cluster'+str(cluster)+'_user_id'].append(_complete_dataset['user_id'][dataset.index(dataset[sentence])])
                 
                w=subject(dataset[sentence],vocabulary)
                if total_feature.get(w) == None :
                        total_feature[w] = 1
                        total_data[cluster]+=1
                else :
                        total_feature[w] += 1
                        total_data[cluster]+=1
                        
            pourcentage[cluster].append(total_feature.copy())
            _cluster_info['cluster'+str(cluster)+'_total_feature']=""
            for k in total_feature :
                    _cluster_info['cluster'+str(cluster)+'_total_feature']+=str(k)
            
            total_feature.clear()

            _cluster_info['cluster'+str(cluster)+'_date']=date[0]
            _cluster_info['cluster'+str(cluster)+'_famousTweetsID']=getMaxFollowerTweet(_cluster_info['cluster'+str(cluster)+'_tweets'],_cluster_info['cluster'+str(cluster)+'_followers_count'])
            _cluster_info['cluster'+str(cluster)+'_famousUserID']=getMaxFollowerTweet(_cluster_info['cluster'+str(cluster)+'_tweets'],_cluster_info['cluster'+str(cluster)+'_user_id'])
            #print("Cluster ",cluster," compute popularity :",total_data[cluster],"*",len(list(set(_cluster_info['cluster'+str(cluster)+'_user_id']))),"/",len(dataset))
            _cluster_info['cluster'+str(cluster)+'_popularity']=(2*total_data[cluster]+4*len(list(set(_cluster_info['cluster'+str(cluster)+'_user_id']))))/(len(dataset)+nb_user)
            _cluster_info['cluster'+str(cluster)+'_lenght']=total_data[cluster]

        for cluster in pourcentage :
            for key in pourcentage[cluster] :
                lastlen = 999
                for char in key :
                    key[char] = "{:.1f}".format((key[char]/total_data[cluster])*100)
                    if len(char) <= lastlen:
                        lastlen = len(char)
                        bestChar = char
                #print(bestChar)

            _cluster_info['cluster'+str(cluster)+'_feature']=bestChar

        #for cluster in pourcentage :
        #    print("cluster",cluster," : ",pourcentage[cluster]," % for ",total_data[cluster]," tweets in the cluster")
        
        print("--- Clustering finish in %s seconds ---" % (time.time() - start_time))
        print("NUMBE OF CLUSTERS : ",n_clusters_," NUMBER OF SAMPLES :",len(dataset))
        for cluster in range(n_clusters_):
                print("Cluster ",cluster," popularity :",_cluster_info['cluster'+str(cluster)+'_popularity'],"lenght : ",_cluster_info['cluster'+str(cluster)+'_lenght'])
                print("Cluster ",cluster," Feature :",_cluster_info['cluster'+str(cluster)+'_feature'])
                print("Cluster ",cluster," Date :",_cluster_info['cluster'+str(cluster)+'_date'])
                print("Cluster ",cluster," All Feature :",_cluster_info['cluster'+str(cluster)+'_total_feature'])
                #print("Cluster ",cluster," famous tweet id :",_cluster_info['cluster'+str(cluster)+'_famousTweetsID'])
                #print("Cluster ",cluster," famous user id :",_cluster_info['cluster'+str(cluster)+'_famousUserID'])
                #url = "https://twitter.com/"+str(_cluster_info['cluster'+str(cluster)+'_famousUserID'])+"/status/"+str(_cluster_info['cluster'+str(cluster)+'_famousTweetsID'])
                #print("Url of the famous tweet :",url)
        
        print("")
        
        print("SQL insert ",date," start at %s seconds ---" % (time.time() - start_time))
        
        insertEvent(_cluster_info,currentCollection)

        print("clustering per days ",date," finish in %s seconds ---" % (time.time() - start_time))
        
        _complete_dataset.clear()
        dataset.clear()
        _cluster_info.clear()
        pourcentage.clear()

