# Import the Twython class
from twython import Twython
import pymongo
import json
import pandas as pd

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)


    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    # Create our query
    query = {'q': 'since:2020-01-21',
            'result_type': 'recent',
            'count': 200,
            'lang': 'fr'}
print(json.dumps(python_tweets.search(**query)['statuses'][0], indent=4, sort_keys=True))

for i in range(0,1000):
    # Search tweets
    dict_result = {'user': [], 'date': [], 'text': [], 'favorite_count': []}

    for status in python_tweets.search(**query)['statuses']:
        dict_result['user'].append(status['user']['screen_name'])
        dict_result['date'].append(status['created_at'])
        dict_result['text'].append(status['text'])
        dict_result['favorite_count'].append(status['favorite_count'])
#       dict_result['entities'].append(status)
#        print(json.dumps(dict_result, indent=4, sort_keys=True))
#    for cle in status:
#        print(cle)
        
    print("---------------------------------------------")

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_result)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    df.head(5)
    print(dict_result['user'][0])
    print(i)
    
#    print(json.dumps(dict_result, indent=4, sort_keys=True))



# MongoDB connection info
hostname = 'mongodb-[projetagp].alwaysdata.net'
port = 27017
username = 'projetagp'
password = 'projet2020'
databaseName = 'projetagp_mongo'

# connect with authentication
client = MongoClient(hostname, port, connect=True)
db = client[databaseName]
db.authenticate(username, password)
