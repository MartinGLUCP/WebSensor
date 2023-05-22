
import psycopg2
from configparser import ConfigParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

#TELECHARGER database.ini sur git

"""
FONCTIONS DISPONIBLENT :

    config : utiliser pour configurer la connection avec le fichier database.ini
    configIfNoDatabase : configure connection si il n'y a pas de database
    connect() : fct de connection
    createDatabaseWebSensor() : cree la bdd websensor
    create_table_vectors() : cree la table vector
    insert_vector(vector,tweet_content,id_tweet) : Inserer dans la table vectors
    deleteAllVectors():supprime tous les vecteurs
    selectVectors() : select tout les vecteurs

"""

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

def configIfNoDatabase(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if(param[0])!="database" :
                db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
def createDatabaseWebSensor():
    
    conn = None
    vector_id = None
    try:
        # read database configuration
        params = configIfNoDatabase()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        # create a new cursor
        cur = conn.cursor()
        cur.execute("create database WebSensor;")
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
def create_table_vectors():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vectors (
                id_vectors BIGSERIAL PRIMARY KEY,
                vector VARCHAR(500) NOT NULL,
                tweet_content VARCHAR(500) NOT NULL,
                id_tweet BIGINT NOT NULL,
                date DATE not null
        )
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_vector(vector,tweet_content,id_tweet,date):
    """ insert a new vendor into the vectors table """
    sql = "INSERT INTO vectors(vector,tweet_content,id_tweet,date) VALUES('%s',%s,%s,%s);"
    #sql = "INSERT INTO vectors(tweet_content,id_tweet) VALUES('%s',%s) RETURNING vectors_id;" % (tweet_content,id_tweet)
    #print(sql)
    conn = None
    vector_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql,(vector,tweet_content,id_tweet,date))
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    #return vector_id

def deleteAllVectors():
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM vectors")
        # get the number of updated rows
        #rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    #return rows_deleted
            
def selectVectors():
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("SELECT * FROM vectors")

        conn.commit()
        vectors_records = cur.fetchall() 
        """
        print("Print each row and it's columns values")
        for row in vectors_records:
            print("Id = ", row[0], "\n")
        """            
        # Close communication with the PostgreSQL database
        cur.close()
        return vectors_records
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
#deleteAllVectors()
#createDatabaseWebSensor()
#create_table_vectors()
#selectVectors()
