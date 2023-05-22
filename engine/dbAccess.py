#pip install mysql-connector
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="websensor"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

req = "INSERT INTO tweet (tweet_id,tweet_text,user,followers_count, verified, date, retweeted) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = [("165","Hey Salut a tous les amis, c'est david lafarge pokemon avec miss jirachi","David","15","1","2020-06-06","0"),
       ("59","COUCOU","Miss Jirachi","999","1","2020-06-06","0"),
       ("955","Lache poce blo si t'a aimé vidéo","Ibra","549848","1","2020-06-06","1")]
mycursor.executemany(req,val)

mydb.commit()

print(mycursor.rowcount, "données inséréesé")

mycursor.execute("SELECT * FROM tweet")

for x in mycursor:
    print(x)


delete = "DELETE FROM tweet WHERE tweet_id IN ('165','59','955')"
mycursor.execute(delete)

mydb.commit()
print(mycursor.rowcount, "données supprimées")
