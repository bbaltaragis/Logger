import sqlite3
import os
import sys
import time
import datetime
import hashlib

def create_anomaly_reference_table():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE AnomalyReference
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, hash TEXT, pattern TEXT, last_occured TEXT, plaintext TEXT, root_cause TEXT, resolution_steps TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)



def create_anomalycomment_table():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE AnomalyComments
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, anomaly_id integer, comment TEXT, username TEXT, active INTEGER)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

def create_goodlogs_table():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE GoodLogs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, name text, pattern text, frequency integer, last_occured text, plaintext TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

#create a table for historical anomaly logs
def create_historical_anomalies_table():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE HistoricalAnomalies
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, anomaly_id INTEGER, plaintext TEXT, date_occured TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

#create function to check if logger db exists
def check_db_exists():
    if os.path.exists('Logger.db'):
        return True
    else:
        return False

def create_db():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        conn.commit()
        conn.close()
        create_anomaly_reference_table()
        create_anomalycomment_table()
        create_goodlogs_table()
        create_historical_anomalies_table()
        print("success")
    except sqlite3.Error as e:
        print(e)

def hash_string(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

#select anomalyreference and goodlogs and return as json
def select_dashboard():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("SELECT * FROM AnomalyReference")
        anomalycomments = c.fetchall()
        c.execute("SELECT * FROM GoodLogs")
        goodlogs = c.fetchall()
        conn.commit()
        conn.close()
        return {"anomalyreference": anomalyreference_to_json(anomalycomments), "goodlogs": goodlogs_to_json(goodlogs)}
    except sqlite3.Error as e:
        print(e)

#create a function to turn anomalyreference into json
def anomalyreference_to_json(anomalyreference):
    json_anomalyreference = []
    for anomaly in anomalyreference:
        json_anomalyreference.append({"id": anomaly[0], "name": anomaly[1], "hash": anomaly[2], "pattern": anomaly[3], "last_occured": anomaly[4], "plaintext": anomaly[5], "root_cause": anomaly[6], "resolution_steps": anomaly[7]})
    return json_anomalyreference
#creat a function to turn goodlogs into json
def goodlogs_to_json(goodlogs):
    json_goodlogs = []
    for log in goodlogs:
        json_goodlogs.append({"id": log[0], "hash": log[1], "name": log[2], "pattern": log[3], "frequency": log[4], "last_occured": log[5], "plaintext": log[6]})
    return json_goodlogs

#create a function to convert historical anomalies to json
def historical_anomalies_to_json(historical_anomalies):
    json_historical_anomalies = []
    for anomaly in historical_anomalies:
        json_historical_anomalies.append({"id": anomaly[0], "anomaly_id": anomaly[1], "plaintext": anomaly[2], "date_occured": anomaly[3]})
    return json_historical_anomalies

#create a function to convert anomalycomments to json
def anomalycomments_to_json(anomalycomments):
    json_anomalycomments = []
    for comment in anomalycomments:
        json_anomalycomments.append({"id": comment[0], "anomaly_id": comment[1], "comment": comment[2], "username": comment[3], "active": comment[4]})
    return json_anomalycomments
#select * from anomalyreference and historicalanomalies where anomaly_id = id
def select_anomaly_reference_and_historical_anomalies(id):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("SELECT * FROM AnomalyReference where id = {}".format(id))
        result = c.fetchall()
        c.execute("SELECT * FROM HistoricalAnomalies where anomaly_id = {}".format(id))
        historical_anomalies = c.fetchall()
        c.execute("SELECT * FROM AnomalyComments where anomaly_id = {}".format(id))
        comments = c.fetchall()
        conn.commit()
        conn.close()
        
        if result == [] and historical_anomalies == []:
            return {"error": "No data found"}
            
        return {"anomalyReference": anomalyreference_to_json(result), "historicalAnomalies": historical_anomalies_to_json(historical_anomalies), "anomalyComments": anomalycomments_to_json(comments)}
    except sqlite3.Error as e:
        print(e)
        

#create a function to insert anomalyreference
def insert_anomalyreference(name, hash, pattern, last_occured, plaintext, root_cause, resolution_steps):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO AnomalyReference (name, hash, pattern, last_occured, plaintext, root_cause, resolution_steps) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, hash, pattern, last_occured, plaintext, root_cause, resolution_steps))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

#insert into historicalanomalies
def insert_historicalanomalies(anomaly_id, plaintext, date_occured):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO HistoricalAnomalies (anomaly_id, plaintext, date_occured) VALUES ({}, '{}', '{}')".format(anomaly_id, plaintext, date_occured))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

#function to get current datetime
def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#create a function to check if anomlyhash exists based on the hash, if true insert result into historicalanomalies
def check_anomalyhash(hash):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("SELECT TOP 1 * FROM AnomalyReference WHERE hash = '{}'".format(hash))
        result = c.fetchall()
        if result:
            c.execute("INSERT INTO HistoricalAnomalies (anomaly_id, plaintext, date_occured) VALUES ('{}', '{}', '{}')".format(result[0][0], result[0][5], result[0][4]))
            conn.commit()
            conn.close()
            return True
        else:
            conn.commit()
            conn.close()
            return False
    except sqlite3.Error as e:
        print(e)

#create a function to insert into anomalycomments
def insert_anomalycomments(anomaly_id, comment, username):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO AnomalyComments (anomaly_id, comment, username) VALUES ('{}', '{}', '{}')".format(anomaly_id, comment, username))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def update_rootcause(id, root_cause):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("UPDATE AnomalyReference SET root_cause = '{}' WHERE id = {}".format(root_cause, id))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def update_resolutionsteps(id, resolution_steps):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("UPDATE AnomalyReference SET resolution_steps = '{}' WHERE id = {}".format(resolution_steps, id))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def insert_goodlogs(hash, name, pattern, plaintext):
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO GoodLogs (hash, name, pattern, plaintext) VALUES ('{}', '{}', '{}', '{}')".format(hash, name, pattern, plaintext))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

#SEEDING TEST DATA

#create a function to seed goodlogs
def seed_goodlogs():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO GoodLogs (hash, name, pattern, frequency, last_occured, plaintext) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(hash_string("test"), "test", "test", 1, get_current_datetime(), "test"))
        c.execute("INSERT INTO GoodLogs (hash, name, pattern, frequency, last_occured, plaintext) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(hash_string("test2"), "test2", "test2", 1, get_current_datetime(), "test2"))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def fill_anomalyreference():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO AnomalyReference (name, hash, pattern, last_occured, plaintext, root_cause, resolution_steps) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format("test", hash_string("test"), "test", "test", "test", "test", "test"))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def fill_anomalycomments():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO AnomalyComment (anomaly_id, comment_plaintext) VALUES ('{}', '{}')".format(1, "test"))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)

def fill_historicalanomalies():
    try:
        conn = sqlite3.connect('Logger.db')
        c = conn.cursor()
        c.execute("INSERT INTO HistoricalAnomalies (anomaly_id, plaintext, date_occured) VALUES ('{}', '{}', '{}')".format(1, "test", "test"))
        conn.commit()
        conn.close()
        print("success")
    except sqlite3.Error as e:
        print(e)