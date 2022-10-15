#!/usr/bin/python

from flask import Flask, jsonify, request
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

#disable jsonify's dict re-ordering
application.config['JSON_SORT_KEYS'] = False


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


@application.route('/formtest1', methods=['POST'])
def formtest():
    if request.method == "POST":
        print('hfel')
        # getting input with freq = set_freq in HTML form
        a = request.form.get("name") # <--- do whatever you want with that value
        print("Your freq value is " + str(a))
    return jsonify(a)

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



@application.route('/test_fetchsql_parent', methods=['GET'])
def ftn_fetchsql_parent():
    connection, cursor = connect_to_mysql()
    db_name1 = 'rsa_db'
    outputname_userinput = 'result_all_rds_'
    

    #preview list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}parent order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    #print('end', list_existingoutputfiles1)
    
    latest_parenttable_id = list_existingoutputfiles1[-1]
    print("latest_parenttable_id:", latest_parenttable_id)

    cursor.execute(f"SELECT * FROM {db_name1}.{outputname_userinput}parent where parenttable_id = {latest_parenttable_id};")
    result = cursor.fetchall() 
    print(type(result)) 

    connection.close()

    return jsonify(result) #nicer, can disable re-ordering in app.config?
    #return json.dumps(result)


@application.route('/test_fetchsql', methods=['GET'])
def ftn_fetchsql():
    connection, cursor = connect_to_mysql()
    db_name1 = 'rsa_db'
    outputname_userinput = 'result_all_rds_'
    

    #preview list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}parent order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    #print('end', list_existingoutputfiles1)
    
    latest_parenttable_id = list_existingoutputfiles1[-1]
    print("latest_parenttable_id:", latest_parenttable_id)

    #try get multiple data tables (in array/list)
    cursor.execute(f"SELECT ticker_id, symbol, mentions, concat('$', format(market_cap/1000000000, 2), 'B') as market_cap, latest_price, change_percent, pe_ratio, company_name, datetime, parenttable_id from {db_name1}.{outputname_userinput}child where parenttable_id = {latest_parenttable_id} limit 50;")
    result = cursor.fetchall() 
    print(type(result)) 

    connection.close()

    return jsonify(result) #nicer, can disable re-ordering in app.config?
    #return json.dumps(result)
    

        

# run the app.
if __name__ == "__main__":
    # ftn_rsa1()

    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    
    #application.run(threaded=True) #threaded=True to try keep persistent connection with mysql = OK, now try application.run() only
    # application.run()
    application.run(host='0.0.0.0', port=5000)#, debug=False, threaded=False)