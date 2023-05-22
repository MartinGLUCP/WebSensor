#pip install mysql-connector
import mysql.connector
from pymongo import MongoClient
import json
from connectMongo import getTweetById
import operator
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="websensor"
)



def insertEvent(_clusters_info,currentCollection):
    req = "INSERT INTO `event`(`features_event`, `short_features_event`, `name`, `total_popularity`) VALUES (%s, %s, %s, %s)"
    events = []
    mycursor = mydb.cursor()
    for i in range(_clusters_info['n_clusters']):
        if str(_clusters_info["cluster"+str(i)+"_total_feature"]) != "" and str(_clusters_info["cluster"+str(i)+'_feature']) != "" :
                features_event = str(_clusters_info["cluster"+str(i)+"_total_feature"])
                short_features_event = str(_clusters_info["cluster"+str(i)+'_feature'])
                total_popularity = _clusters_info["cluster"+str(i)+'_popularity']
                famous_idTweet = _clusters_info["cluster"+str(i)+'_famousTweetsID']

                mycursor2 = mydb.cursor()
                    
                mycursor2.execute("SELECT features_event,total_popularity FROM event where short_features_event='"+short_features_event+"'")

                myresult = mycursor2.fetchone()

                    #print(myresult)
                if myresult == None :
                        #print("select on Event",myresult)
                    try:
                        mycursor.execute(req,tuple((features_event,short_features_event,'',total_popularity))) #append data
                        mydb.commit()          
                    except:
                        mydb.rollback()
                        
                        
                else :
                    _concatenate_features=myresult[0]+" "+features_event
                    copy = _concatenate_features.split(" ")
                    _unique_features = list(set(copy.copy()))
                    _unique_concatenate_features =""
                    for i in _unique_features :
                        _unique_concatenate_features += str(i)+' '
                    _unique_concatenate_features.rstrip()
                    sqlUpdate = "UPDATE event SET total_popularity ="+str(float(myresult[1]+total_popularity))
                    sqlUpdate += ",features_event='"+_unique_concatenate_features+"' "
                    sqlUpdate += "WHERE short_features_event ='"+short_features_event+"'"
                    try :
                        mycursor.execute(sqlUpdate)
                        mydb.commit()
                    except:
                        print("Error Event")
                        mydb.rollback()    
                insertTweet(famous_idTweet,currentCollection)
    insertPopularity(_clusters_info)
            
    

def insertTweet(idTweet,currentCollection):
    mycursor3=mydb.cursor()
    req = "INSERT INTO `tweet`(`tweet_id`, `tweet_text`, `user_id`, `user`, `user_name`, `followers_count`, `location`, `verified`, `coordinates`, `date`, `favorite_count`, `retweet_count`, `in_reply_to_id`, `retweeted`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    tweets = []
    _tweet_info = getTweetById(idTweet,currentCollection)
    #print("_tweet_info : ",_tweet_info)
    if _tweet_info != None:
        
        ts = time.strftime('%Y-%m-%d', time.strptime(_tweet_info["date"],'%a %b %d %H:%M:%S +0000 %Y'))
        
        val = (_tweet_info['tweet_id'],_tweet_info['text'],_tweet_info['user_id'],_tweet_info['user'],_tweet_info['user_name'],_tweet_info['followers_count'],_tweet_info['location'],_tweet_info['verified'],str(_tweet_info['coordinates']),ts,_tweet_info['favorite_count'],_tweet_info['retweet_count'],_tweet_info['in_reply_to_id'],_tweet_info['retweeted'])
        
        try:
            #print(val)
            mycursor3.execute(req,tuple(val))
            mydb.commit()
        except :
            print("Error Tweet")
            mydb.rollback()

def insertPopularity(_clusters_info):
    req = "INSERT INTO `popularity`( `popularity_date`, `ranked`, `number`, `tweet_id`, `event_id`) VALUES  (%s, %s, %s, %s, %s)"
    mycursor=mydb.cursor()
    popularity = []
    date3=""
    for i in range(_clusters_info['n_clusters']):
        if str(_clusters_info["cluster"+str(i)+"_total_feature"]) != "" and str(_clusters_info["cluster"+str(i)+'_feature']) != "" :
            short_features_event = str(_clusters_info["cluster"+str(i)+'_feature'])
            
            number = _clusters_info["cluster"+str(i)+'_popularity']
            date2 = _clusters_info["cluster"+str(i)+'_date']
            tweet_id = _clusters_info["cluster"+str(i)+'_famousTweetsID']

            mycursor.execute("SELECT event_id FROM event where short_features_event='"+short_features_event+"'")

            myresult = mycursor.fetchone()
            
            if myresult != None :
                
                try :
                    #print("select on Event",myresult)
                     mycursor.execute(req,tuple((date2,0,number,tweet_id,myresult[0]))) #append data
                     mydb.commit()
                except:
                    print("Error Popularity")
                    mydb.rollback()

    #Classement
    date3=_clusters_info["cluster"+str(i)+'_date']
    
    mycursor.execute("SELECT popularity_id,number FROM popularity where popularity_date='"+date3+"'")

    myresult2 = mycursor.fetchall()

    d ={}
    j=1
    
    for x in myresult2 :
        d[x[0]]=float(x[1])
    
    sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1),reverse=True))
    #print(d)
    #print(sorted_d)

    
    for key in sorted_d :
        if j<11 :
            sqlUpdate = "UPDATE popularity SET ranked ="+str(j)
            sqlUpdate += " WHERE popularity_id ='"+str(key)+"'"
            #print(sqlUpdate)
            try :
                mycursor.execute(sqlUpdate)
                mydb.commit()
            except:
                print("Error classement")
                mydb.rollback()
            j+=1
        else :
            break
    
"""
_clusters_info={'n_clusters':3,'cluster0_popularity':10,'cluster0_total_feature':'zaza zizi','cluster0_date':'2014-05-05','cluster0_famousTweetsID':'1248831622625009665'
               ,'cluster0_famousUserID':'1122134867800678400','cluster0_feature':'zaza'
               ,'cluster1_popularity':30,'cluster1_total_feature':'zaza zouzou','cluster1_date':'2014-05-05','cluster1_famousTweetsID':'1248999470018097153'
               ,'cluster1_famousUserID':'103781192','cluster1_feature':'zizi',
               'cluster2_popularity':40,'cluster2_total_feature':'zuzu zuzu','cluster2_date':'2014-05-05','cluster2_famousTweetsID':'1249123042363617281'
               ,'cluster2_famousUserID':'850514563237900288','cluster2_feature':'zaza'
               }

_clusters_info={'n_clusters':1,'cluster0_popularity':10,'cluster0_total_feature':'zaza zizi','cluster0_date':'2014-05-05','cluster0_famousTweetsID':'1248831622625009665'
               ,'cluster0_famousUserID':'1122134867800678400','cluster0_feature':'zaza'}

insertEvent(_clusters_info)
"""
