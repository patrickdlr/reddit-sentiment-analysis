#!/usr/bin/python

from flask import Flask, jsonify
import csv, os, sys
import pathlib
from flask_cors import CORS
import flask_sqlalchemy# import SQLAlchemy
import pprint
import json #for json.dumps (to display json file with string/list in neater form)

print('sys.path: ' + str(sys.path))
print('os.path: ' + str(os.path))
sys.path.insert(1, r'rsa') #insert a folder, not .py..?
from rsa import *
#import rsa #doesn't work..

'''*****************************************************************************
# variables of file paths & options
*****************************************************************************'''
path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__))))
path_csvfiles_and_result_all_010 = '/csvfiles/result_all_010.csv'
path_repo_and_csvfiles_and_result_all_010 = str(pathlib.Path(path_repo + path_csvfiles_and_result_all_010))
# print(path_repo)
# print(path_csvfiles_and_result_all_010)
# print(path_repo_and_csvfiles_and_result_all_010)

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Use CORS..?
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'



'''*****************************************************************************
# SQLAlchemy (test)
*****************************************************************************'''
MYSQL_HOST_RDS=os.environ.get('MYSQL_HOST_RDS')
MYSQL_USER_RDS=os.environ.get('MYSQL_USER_RDS')
MYSQL_PASSWORD_RDS=os.environ.get('MYSQL_PASSWORD_RDS')
MYSQL_DB_NAME = 'rsa_db'

application.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{MYSQL_USER_RDS}:{MYSQL_PASSWORD_RDS}@{MYSQL_HOST_RDS}/{MYSQL_DB_NAME}'
db = flask_sqlalchemy.SQLAlchemy(application)

application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True



'''*****************************************************************************
# accessing mysql (test)
#get data in dictionary/list form
*****************************************************************************'''
import pymysql
def connect_to_mysql():
    connection = pymysql.connect(
                                host=os.environ.get('MYSQL_HOST_RDS'),
                                user=os.environ.get('MYSQL_USER_RDS'),
                                password=os.environ.get('MYSQL_PASSWORD_RDS'),
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor




@application.route("/home")
@application.route("/")
def hello_world():
    return "<p>Hello, World!kjjk<p><div style='position:fixed; left: 10px; color:red;'>bakaffggf</div>"


data1 = 'hello world1!!!!!!'
@application.route('/fetchtest', methods=['GET'])
def fetchtest():
    print('sadfdf')
    return jsonify({'key1' : data1, 'key2':'002 bkend'})


@application.route('/readtxtfile', methods=['GET'])
def readtxtfile():
    with open('sampletext.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return jsonify(lines)
    return jsonify("No text file result FOUND")


##good
@application.route('/test_fetchcsvfile', methods=['GET'])
def ftn_fetchcsvfile():
    
    
    with open(path_repo_and_csvfiles_and_result_all_010,'r') as f:
        lines = f.readlines()
    
    string1 = ""
    for a in lines[0:6]:
        string1 += a
        string1 += "</br>"


    for a in lines[7:]:
        lines[lines.index(a)] = "%10s" % a
        string1 += lines[lines.index(a)]
        string1 += "</br>"

    # return jsonify(f"<p>{string1}</p>") #add jsonify to work with front end..?
    # return jsonify(string1)
    return json.dumps(string1) #nicer, prints neatly like seen in python console

    
@application.route('/test_fetchsql', methods=['GET'])
def ftn_fetchsql():
    connection, cursor = connect_to_mysql()
    database_name1 = 'rsa_db'

    # 1 - get a list of existing saved tables that contains given outputname_userinput
    list_existingoutputfiles1 = [] 
    outputname_userinput = "result_all_rds_"
    cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND table_name like '{outputname_userinput}%';")
    result = cursor.fetchall()

    # 2 -get latest output
    list_existingoutputfiles1 = [list(a.values())[0] for a in result]
    latest_output = str(list_existingoutputfiles1[-1])
    print(latest_output)


    cursor.execute(f"SELECT * from {database_name1}.{latest_output} where number < 20;")
    result = cursor.fetchall()  

    connection.close()

    return jsonify(result) #nicer
    # return json.dumps(result) 
    
    



        

# run the app.
if __name__ == "__main__":
    # ftn_rsa1()

    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    
    #application.run(threaded=True) #threaded=True to try keep persistent connection with mysql = OK, now try application.run() only
    application.run()