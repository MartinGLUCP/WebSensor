from pymongo import MongoClient
import json
import time

#pour terminal mongo
#cd C:\Program Files\MongoDB\Server\4.2\bin
#mongod
#(dans un autre terminal)
#cd C:\Program Files\MongoDB\Server\4.2\bin 
#mongo
#use webSensor      utilise la base
#db.createCollection("tweet")   pour créer une collection
#db.tweet.find()  pour afficher la collection (= table)


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

def getTweetById(idTweet,currentCollection):
    collection = db[currentCollection]
    return collection.find_one( { "tweet_id": str(idTweet) } )

def saveInTweet(post):
    collection = db.tweet
    collection.insert_one(post)
    post.pop('_id', None)

def saveInCoronavirus(post):
    collection = db.coronavirus
    collection.insert_one(post)
    post.pop('_id', None)

def saveInExtrait(post):
    collection = db.extrait
    collection.insert_one(post)
    post.pop('_id', None)

def getLastTweetIdExtrait():
    collection = db.extrait
    tweet_id = ""
    for tweet in collection.find().sort([('tweet_id', 1)]).limit(1):
        tweet_id = tweet['tweet_id']
    return tweet_id

def getLastTweetId():
    #mongo command : db.collection.find().sort( { _id : -1 } ).limit(1);
    collection = db.coronavirus
    tweet_id = ""
    for tweet in collection.find().sort([('_id', -1)]).limit(1):
        print(tweet)
        tweet_id = tweet['tweet_id']
    return tweet_id

def selectAll(currentCollection):
    collection = db[currentCollection]
    _tweets = {}
    _tweets['text']=[]
    _tweets['tweet_id']=[]
    _tweets['followers_count']=[]
    _tweets['date']=[]
    _tweets['user_id']=[]
    #selection de 1000 tweets trier par tweet_id du plus récent au plus vieux .limit(3000)
    for tweet in collection.find().sort([('tweet_id', 1)]).limit(30000):
        ts = time.strftime('%Y-%m-%d', time.strptime(tweet["date"],'%a %b %d %H:%M:%S +0000 %Y'))
        
        _tweets['text'].append(str(tweet['text']))
        _tweets['tweet_id'].append(str(tweet['tweet_id']))
        _tweets['followers_count'].append(str(tweet['followers_count']))
        _tweets['date'].append(str(ts))
        _tweets['user_id'].append(str(tweet['user_id']))
        
    return _tweets

"""
#file = open("dataset.txt", "w")
##Appel de test :
count = 0
tweets = selectAll()
print(len(tweets['text']))
for tweet in tweets['text']:
    #file.write(str(tweet.encode('ascii', 'ignore').decode('utf-8', 'ignore')))
    #file.write(" ")
    if "coronavirus" in str(tweet.encode('ascii', 'ignore').decode('utf-8', 'ignore')) :
        count +=1    
#file.close()

print(count)
"""
#print(getTweetById(1248999470018097153))
