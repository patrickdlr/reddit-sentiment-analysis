#!/usr/bin/python

from flask import Flask, jsonify
import csv, os, sys
# from pathlib import Path, PurePosixPath
import pathlib
from flask_cors import CORS


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
    
    csvfile1 = pathlib.PurePosixPath(r'csvfiles/result_test_010.csv')
    csvfile2 = pathlib.PurePosixPath(r'/csvfiles/result_test_010.csv')
    
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

    return jsonify(f"<p>{string1}</p>") #add jsonify to work with front end..?


    #headers=lines[0].rstrip().split(',') # rstrip removes end-of-line chars
    #numLines = len(lines)
    #linelist = [x.rstrip().split(',') for x in lines[1:numLines+1]]    
    ## create lineList to include only numLines elements
    #outputDict = {keyVal:[x[idx] for x in linelist if len(x)==len(headers)] for idx,keyVal in enumerate(headers)}   

    ## list comprehension within dictionary comprehension to split each element by its header and create dictionary of lists 
    ## print(outputDict)
    
    ## for u in outputDict['Symbol']:
    ##     us_local.add(u)

    #aka = outputDict['Symbol'][:10]
    #print('aka: ' + str(aka))

    #return jsonify(aka) #jsonify to avoid unexpected token SyntaxError...
        

# run the app.
if __name__ == "__main__":
    # ftn_rsa1()

    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True

    application.run()
    