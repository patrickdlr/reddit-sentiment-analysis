#!/usr/bin/python
'''*****************************************************************************
Purpose: To analyze the sentiments of the reddit
This program uses Vader SentimentIntensityAnalyzer to calculate the ticker compound value. 
You can change multiple parameters to suit your needs. See below under "set program parameters."
Implementation:
I am using sets for 'x in s' comparison, sets time complexity for "x in s" is O(1) compare to list: O(n).
Limitations:
It depends mainly on the defined parameters for current implementation:
It completely ignores the heavily downvoted comments, and there can be a time when
the most mentioned ticker is heavily downvoted, but you can change that in upvotes variable.
Author: github:asad70
****************************************************************************'''
#imports by asad70
from operator import ne
from unittest import expectedFailure
import praw
from pymysql import NULL
from data import *
import time
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji    # removes emojis
import re   # removes links
import en_core_web_sm
import string

#imports (to build flask app with csv/mysql database, api data collection, schedules, threading, multiprocessing) by me
import nltk
nltk.download('wordnet', quiet=True) #what does this do?
nltk.download('vader_lexicon', quiet=True)
from prawcore.exceptions import Forbidden
from multiprocessing import Process
from threading import Thread
import datetime
import pymysql
import os, sys, csv, requests, schedule, pathlib, pprint, urllib.request, ast


'''*****************************************************************************
# program options & environment variables
*****************************************************************************'''
isPrint_logs = True
use_sentiment_analysis_and_visualization = False
storagetype = "mysql"
write_empty_newoutputfile = False #default: False

max_output_amount = 300
if max_output_amount < 1: raise ValueError('max output amount cannot be <1')

IEX_TOKEN = os.environ.get('IEX_TOKEN')
IEX_TOKEN = F'?token={IEX_TOKEN}' 
IEX_TOKEN_SANDBOX = os.environ.get('IEX_TOKEN_SANDBOX')
IEX_TOKEN_SANDBOX = F'?token={IEX_TOKEN_SANDBOX}' 


'''*****************************************************************************
# csv (for data storage):
# variables of csv file paths 
*****************************************************************************'''
path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + '/..'))
path_csvfiles = '/csvfiles'
path_repo_and_csvfiles = str(pathlib.Path(path_repo + path_csvfiles))


'''*****************************************************************************
# mysql (for data storage):
# variables + establish connection to mysql database (can't do variable initialization idk why)
# program options
*****************************************************************************'''
def connect_to_mysql():
    connection = pymysql.connect(
                                host=os.environ.get('MYSQL_HOST_RDS'),
                                user=os.environ.get('MYSQL_USER_RDS'),
                                password=os.environ.get('MYSQL_PASSWORD_RDS'),
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    return connection, cursor

if storagetype == "mysql":
    connection, cursor = connect_to_mysql()
    # db_name1 = 'rsa_db_onetableversion'
    # db_name1 = 'test_db1'
    db_name1 = 'rsa_db'

'''*****************************************************************************
# Parameters for main function
*****************************************************************************'''
input_api_nasdaq = 'api.nasdaq.com'

output_filename0 = 'result_test_'
output_filename1 = 'result_all_'
output_filename1_RDS = 'result_all_rds_'
output_filename2 = 'result_200b_'
output_filename3 = 'result_15b_'
output_filename4 = 'result_4b_'
output_filename4_RDS = 'result_4b_rds_'
output_filename4_300run = 'result_4b_300run_'
output_filename5 = 'result_4m_'

subs_specificlist1 = ['wallstreetbets']
subs_specificlist2 = ['Stocks', 'Bitcoin', 'Wallstreetbetsnew', 'PennyStocks', 'algotrading', 'Economics', 'investing', 'Pennystocks', 'StockMarket', 'stocks', 'Investing', 'pennystocks', 'Options', 'AlgoTrading', 'wallstreetbets', 'Cryptocurrency', 'WallStreetBets']
subs_specificlist3 = ['Bitcoin', 'Cryptocurrency', 'DayTrading']

subs_membercount_min1 = 0
subs_membercount_min2 = 600000
subs_membercount_min3 = 1000000

marketcap_min0 = 0
marketcap_min1 = 1000
marketcap_min2 = 1000000000

marketcap_max1 = 35000000000000 #all
marketcap_max2 = 200000000000
marketcap_max3 = 15000000000
marketcap_max4 = 4000000000
marketcap_max5 = 4000000

#testing line 306 #limit amount of symbols/picks printed
                  # if top_picks.index(i) >= picks: #testing
                  #     break


'''*****************************************************************************
# "worker" functions
*****************************************************************************'''
def ftn_rsa1():
    print('ftn_rsa1() on rsa.py used')

def warning_maxoutputexceeded(list_existingoutputfiles1, max_output_amount):
    if len(list_existingoutputfiles1) > max_output_amount:
        for r in range(3): #input() doesn't work in multithreading mode
            print(f"Note: output file count: {len(list_existingoutputfiles1)} > max_output_amount: {max_output_amount}")
            a = input("Max # of allowed output files is LOWER than existing output files. Proceeding will limit existing output files by deleting the oldest, excessive output files. Do you want to continue? (Y/N) ")
            
            if a.lower() == "y" or a.lower() == "yes":
                break
            elif a.lower() == "n" or a.lower() == "no" or r >= 2:
                print("User chose to not continue.. stopping the program now. Review the 'max output amount' variable.")
                sys.exit()
                #os._exit() #exits the whole process i think.
            else:
                continue 
    

# JUST ADDED
# for prepare_variables1, deleteandrename_existing.. functions
def check_exists_3tables(outputname_userinput):
    '''*****************************************************************************
    ### 0 - check if database, parent table, child table exist or doesn't exist yet
    *****************************************************************************'''
    exists_database = None
    exists_parenttable = None
    exists_childtable = None

    ### 0
    #check if database exists
    cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name1}';")
    result = cursor.fetchall()
    if result == () or result == None: exists_database = False
    else: exists_database = True

    #check if parent table exists
    cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND TABLE_NAME = '{outputname_userinput}parent';")
    result = cursor.fetchall()
    if result == () or result == None: exists_parenttable = False
    else: exists_parenttable = True

    #check if child table exists
    cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND TABLE_NAME = '{outputname_userinput}child';")
    result = cursor.fetchall()
    if result == () or result == None: exists_childtable = False
    else: exists_childtable = True


    return exists_database, exists_parenttable, exists_childtable

# OLD
def prepare_variables1_csv_and_sql(storagetype, outputname_userinput, max_output_amount):
    '''*****************************************************************************
    # Preparing latest outputname_userinput filename
    # Parameter: outputname_userinput, max_output_amount
    #1 get a list of existing saved output file/table that contains given outputname_userinput = ok
    #1.5 warn the user about max_output_amount deleting the oldest, excessive output files = ok
    #2 get len = ok
    #3 get new ref number (10 if 10 files there already, 10 if 9 there already, 9 if 8 files there already, 1 if 0, 2 if 1) = ok
    #4 get potential outputname_userinput filename.. to be created if program finishes) = ok
    *****************************************************************************'''
    if storagetype != "mysql" and storagetype != "csv":
        print("warning: check your storagetype entry. Could be simply mispelled.")


    #1
    if storagetype == "mysql":
        # 0 - if database doesn't exist yet, create one
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name1}';")
        result = cursor.fetchall()
        if result == () or result == None: 
            print(f"No such database exists. Creating database {db_name1}...")
            cursor.execute(f"CREATE DATABASE {db_name1}")
            print(f"Successfully created {db_name1}")

        # 1 - get a list of existing saved tables that contains given outputname_userinput
        list_existingoutputfiles1 = []    
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '{outputname_userinput}%';")
        result = cursor.fetchall()
        list_existingoutputfiles1 = [list(a.values())[0] for a in result]
        #print('list_existingoutputfiles1 (prepare_variables1_csv_and_sql)'.ljust(55), list_existingoutputfiles1) #log

    if storagetype == "csv":
        # 1
        list_existingoutputfiles1 = []
          
        for a in os.listdir(path_repo_and_csvfiles):
            #print('checking', a, 'with', outputname_userinput) #log
            # if a.startswith(outputname_userinput + '0') or a.startswith(outputname_userinput + '1'): not needed
            if a.startswith(outputname_userinput):
                list_existingoutputfiles1.append(a)

        #print('list_existingoutputfiles1 (prepare_variables1_csv) 1', list_existingoutputfiles1) #log

    # 1.5 - don't use on AWS b/c it prompts user input
    # warning_maxoutputexceeded(list_existingoutputfiles1, max_output_amount)
    
    
    # 2,3
    if len(list_existingoutputfiles1) >= max_output_amount:
        new_ref_number = max_output_amount
    else:
        new_ref_number = len(list_existingoutputfiles1) + 1
    #print('new_ref_number: ', new_ref_number) #log
    

    # 4
    if storagetype == "mysql":
        if new_ref_number < 10:
            outputname_generated = outputname_userinput + '00' + str(new_ref_number)
        elif new_ref_number >= 10 and new_ref_number < 100: 
            outputname_generated = outputname_userinput + '0' + str(new_ref_number)
        elif new_ref_number >= 100 and new_ref_number < 1000:   
            outputname_generated = outputname_userinput + str(new_ref_number)  
        #print('outputname_generated:', outputname_generated) #log

        
    if storagetype == "csv":
        if new_ref_number < 10:
            outputname_generated = path_repo_and_csvfiles + "/" + outputname_userinput + '00' + str(new_ref_number) + '.csv'
        elif new_ref_number >= 10 and new_ref_number < 100: 
            outputname_generated = path_repo_and_csvfiles + "/" + outputname_userinput + '0' + str(new_ref_number) + '.csv'
        elif new_ref_number >= 100 and new_ref_number < 1000:   
            outputname_generated = path_repo_and_csvfiles + "/" + outputname_userinput + str(new_ref_number) + '.csv'
        #print('outputname_generated', outputname_generated) #log

    return outputname_generated, list_existingoutputfiles1, new_ref_number   

# JUST ADDED
def prepare_variables1_sql_parentandchildtables(outputname_userinput, max_output_amount):
    '''*****************************************************************************
    ### 0 - check if database, parent table, child table exist or doesn't exist yet
    ### 1 - get new ref number (set as 1 if tables dont exist OR get latest/highest parenttable_id from child table if exist)
    ### 2 - adjust the new ref number (parenttable_id + 1) -- (using max_output = 10: 10 if parenttable_id = 10 there already, 10 if 9 there already, 9 if 8 files there already, 1 if 0, 2 if 1)
    ### parameters: outputname_userinput, max_output_amount
    ### return variables: new_ref_number
    *****************************************************************************'''
    exists_database, exists_parenttable, exists_childtable = check_exists_3tables(outputname_userinput)

    print("------------------------------------------------------")
    print('prepare_variables1_sql_parentandchildtables()')
    print('outputname_userinput:', outputname_userinput)
    print(f"exists_database={exists_database} | exists_parenttable={exists_parenttable} | exists_childtable={exists_childtable}")
        
    


    ### 1
    new_ref_number = 0
    #select parenttable_id from result_all_child order by parenttable_id desc limit 1;


    #xxx 1
    if exists_database == False and exists_parenttable == False and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0       

    #0xx 2
    if exists_database == True and exists_parenttable == False and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0       


    #0x0 2
    if exists_database == True and exists_parenttable == False and exists_childtable == True:
        #preparevariables1 = ok
        #step 0: get latest/highest parenttable_id from child table for ref number
        sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
        cursor.execute(sql)

        result = cursor.fetchall()
        # pprint.pprint(result)
        #turn into list
        list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
        # remove duplicates
        list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
        print(list_existingoutputfiles1)

        if list_existingoutputfiles1 == []:
            new_ref_number = 0
        else:
            # new_ref_number = list_existingoutputfiles1[-1]
            new_ref_number = len(list_existingoutputfiles1)

        
    #00x 3
    if exists_database == True and exists_parenttable == True and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0
      

    #000 2
    if exists_database == True and exists_parenttable == True and exists_childtable == True:
        #preparevariables1 = ok
        #step 0: get latest/highest parenttable_id from child table for ref number
        sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
        cursor.execute(sql)

        result = cursor.fetchall()
        # pprint.pprint(result)
        #turn into list
        list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
        # remove duplicates
        list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
        print(list_existingoutputfiles1)

        if list_existingoutputfiles1 == []:
            new_ref_number = 0
        else:
            # new_ref_number = list_existingoutputfiles1[-1]
            new_ref_number = len(list_existingoutputfiles1)
   

    ### 2
    if new_ref_number >= max_output_amount:
        print(f'limiting new_ref_number from {new_ref_number} to {max_output_amount}')
        new_ref_number = max_output_amount
    else:
        new_ref_number += 1

    print("new_ref_number set as", new_ref_number)
    return new_ref_number

# OK
def prepare_variables2_additional_info(subs, marketcap_max):
    dt_string = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
    info_subcount = 'Sub count: ' + str(len(subs))
    
    if marketcap_max > 2000000000000: 
        info_marketCap_limit = 'Market Cap min: >2 trillions' 
    else: 
        info_marketCap_limit = 'Market Cap min: ' + str(marketcap_max/1000000000) + ' billion(s)'

    subreddit_count = len(subs)
    return dt_string, info_subcount, info_marketCap_limit, subreddit_count

# OK
def print_logs1(dt_string, outputname_generated, info_subcount, info_marketCap_limit, us):
    if isPrint_logs == True:
        print("------------------------------------------------------")
        print("Date and Time: " + dt_string + " (Beg main)")
        print('Path outputname_userinput: ' + outputname_generated)
        print(info_subcount)
        print(info_marketCap_limit)
        print('Number of tickers found (from input): ' + str(len(us)))

# OK
def data_extractor(reddit, subs, us):
    ##def data_extractor(reddit):

    '''extracts all the data from reddit
    Parameter: reddt: reddit obj
    Return:    posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz
                
                posts: int: # of posts analyzed
                 c_analyzed: int: # of comments analyzed
                 tickers: dict: all the tickers found
                titles: list: list of the title of posts analyzed 
                 a_comments: dict: all the comments to analyze
                 picks: int: top picks to analyze
                 subs: int: # of subreddits analyzed
                picks_ayz: int: top picks to analyze
    '''
 
    '''############################################################################'''      
    #default
    #subs =

    post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}    # posts flairs to search || None flair is automatically considered
    goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
    uniqueCmt = True                # allow one comment per author per symbol
    ignoreAuthP = {'example'}       # authors to ignore for posts 
    ignoreAuthC = {'example'}       # authors to ignore for comment 
    upvoteRatio = 0.5               # upvote ratio for post to be considered, 0.70 = 70%
    ups = 1       # define # of upvotes, post is considered if upvotes exceed this # #20
    limit = 1     # define the limit, comments 'replace more' limit
    upvotes = 1     # define # of upvotes, comment is consi adered if upvotes exceed this #20
    picks = 50     # define # of picks here, prints as "Top ## picks are:" 10
    picks_ayz = 25   # define # of picks for sentiment analysis 5
    

    info_parameters = "upvoteRatio: " + str(upvoteRatio) + " | ups: " + str(ups) + " | limit: " + str(limit) + " | upvotes: " + str(upvotes) + " | picks: " + str(picks) + " | picks_ayz: " + str(picks_ayz) #logprint
    if isPrint_logs == True:
        print(info_parameters)
        print()

    '''############################################################################''' 

    posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
    cmt_auth = {}
    
    for sub in subs:
        try:
            subreddit = reddit.subreddit(sub)
            hot_python = subreddit.hot()    # sorting posts by hot
        
            # Extracting comments, symbols from subreddit
            for submission in hot_python:
                flair = submission.link_flair_text
            
                ####
                ####
                #author = submission.author.name   

                #OR
                try:
                    author = submission.author.name    
                except (AttributeError):
                    #if author == None: ###########possible fix
                    #print(str(submission.author.name), ' --> AttributeErrorignored')
                    continue
                ####
                ####

            
                # checking: post upvote ratio # of upvotes, post flair, and author 
                if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuthP:   
                    submission.comment_sort = 'new'     
                    comments = submission.comments
                    titles.append(submission.title)
                    posts += 1
                    try: 
                        submission.comments.replace_more(limit=limit)   
                        for comment in comments:
                            # try except for deleted account?
                            try: auth = comment.author.name
                            except: pass
                            c_analyzed += 1
                        
                            # checking: comment upvotes and author
                            if comment.score > upvotes and auth not in ignoreAuthC:      
                                split = comment.body.split(" ")
                                for word in split:
                                    word = word.replace("$", "")        
                                    # upper = ticker, length of ticker <= 5, excluded words,                     
                                    if word.isupper() and len(word) <= 5 and word not in blacklist and word in us:
                                    
                                        # unique comments, try/except for key errors
                                        if uniqueCmt and auth not in goodAuth:
                                            try: 
                                                if auth in cmt_auth[word]: break
                                            except: pass
                                        
                                        # counting tickers
                                        if word in tickers:
                                            tickers[word] += 1
                                            a_comments[word].append(comment.body)
                                            cmt_auth[word].append(auth)
                                            count += 1
                                        else:                               
                                            tickers[word] = 1
                                            cmt_auth[word] = [auth]
                                            a_comments[word] = [comment.body]
                                            count += 1   
                    except Exception as e: print(e)

        except Forbidden:
            continue #SKIP SUBreddit that gives off 403 error>..?

    return posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz, info_parameters, upvoteRatio, ups, limit, upvotes

# OK
def print_helper(tickers, picks, c_analyzed, posts, subs, titles, time, start_time):
    '''prints out top tickers, and most mentioned tickers
    
    Parameter:   tickers: dict: all the tickers found
                 picks: int: top picks to analyze
                 c_analyzed: int: # of comments analyzed
                 posts: int: # of posts analyzed
                 subs: int: # of subreddits analyzed
                titles: list: list of the title of posts analyzed 
                 time: time obj: top picks to analyze
                start_time: time obj: prog start time
    Return: symbols: dict: dict of sorted tickers based on mentions
            times: list: include # of time top tickers is mentioned
            top: list: list of top tickers
    '''    
    #global top_picks #only needed for printing

    # sorts the dictionary
    symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
    top_picks = list(symbols.keys())[0:picks]
    seconds_took = (time.time() - start_time) # used to time, before renaming to seconds_took

    info_ittookxseconds = "It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.".format(t=seconds_took, c=c_analyzed, p=posts, s=len(subs)) #log print
    if isPrint_logs == True:
        # print top picks
        #print("It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.".format(t=time, c=c_analyzed, p=posts, s=len(subs)))
        #OR
        #info_ittookxseconds
        print(info_ittookxseconds)

        #print("Posts analyzed saved in titles\n")

        #for i in titles: print(i)  # prints the title of the posts analyzed
    
        print("{} most mentioned tickers: ".format(picks))
    
    times = []
    top = []
    for i in top_picks:
        #testing
        # if top_picks.index(i) >= picks: 
        #     break
        
        #limit amount of symbols/picks printed
        if isPrint_logs == True:
            if top_picks.index(i) < 5: #only print up to 5
                print("{}: {}".format(i,symbols[i]))

        times.append(symbols[i])
        top.append("{}: {}".format(i,symbols[i]))

    return symbols, times, top, info_ittookxseconds, seconds_took

# OK
def sentiment_analysis(picks_ayz, a_comments, symbols, us):
    ##def sentiment_analysis(picks_ayz, a_comments, symbols)
    '''analyzes sentiment anaylsis of top tickers
    
    Parameter:   picks_ayz: int: top picks to analyze
                 a_comments: dict: all the comments to analyze
                 symbols: dict: dict of sorted tickers based on mentions
    Return:      scores: dictionary: dictionary of all the sentiment analysis
    '''
    scores = {}
     
    vader = SentimentIntensityAnalyzer()
    vader.lexicon.update(new_words)     # adding custom words from data.py 
    picks_sentiment = list(symbols.keys())[0:picks_ayz]
    
    for symbol in picks_sentiment:
        stock_comments = a_comments[symbol]
        for cmnt in stock_comments:
    
            emojiless = emoji.get_emoji_regexp().sub(u'', cmnt) # remove emojis
            
            # remove punctuation
            text_punc  = "".join([char for char in emojiless if char not in string.punctuation])
            text_punc = re.sub('[0-9]+', '', text_punc)
                
            # tokenizeing and cleaning 
            tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
            tokenized_string = tokenizer.tokenize(text_punc)
            lower_tokenized = [word.lower() for word in tokenized_string] # convert to lower case
            
            # remove stop words
            nlp = en_core_web_sm.load()
            stopwords = nlp.Defaults.stop_words
            sw_removed = [word for word in lower_tokenized if not word in stopwords]
            
            # normalize the words using lematization
            lemmatizer = WordNetLemmatizer()
            lemmatized_tokens = ([lemmatizer.lemmatize(w) for w in sw_removed])
            
            # calculating sentiment of every word in comments n combining them
            score_cmnt = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
            
            word_count = 0
            for word in lemmatized_tokens:
                if word.upper() not in us:
                    score = vader.polarity_scores(word)
                    word_count += 1
                    for key, _ in score.items():
                        score_cmnt[key] += score[key]    
                else:
                    score_cmnt['pos'] = 2.0               
                    
            # calculating avg.
            try:        # handles: ZeroDivisionError: float division by zero
                for key in score_cmnt:
                    score_cmnt[key] = score_cmnt[key] / word_count
            except: pass
                
            
            # adding score the the specific symbol
            if symbol in scores:
                for key, _ in score_cmnt.items():
                    scores[symbol][key] += score_cmnt[key]
            else:
                scores[symbol] = score_cmnt        
    
        # calculating avg.
        for key in score_cmnt:
            scores[symbol][key] = scores[symbol][key] / symbols[symbol]
            scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])
            
    return scores

# OK
def visualization(picks_ayz, scores, picks, times, top):

    '''prints sentiment analysis
       makes a most mentioned picks chart
       makes a chart of sentiment analysis of top picks
       
    Parameter:   picks_ayz: int: top picks to analyze
                 scores: dictionary: dictionary of all the sentiment analysis
                 picks: int: most mentioned picks
                times: list: include # of time top tickers is mentioned
                top: list: list of top tickers
    Return:       None
    '''
    
    # printing sentiment analysis 
    if isPrint_logs == True:
        print("\nSentiment analysis of top {} picks:".format(picks_ayz))

    df = pd.DataFrame(scores)
    df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/Compound']
    df = df.T
    print('df: ')
    print(df) 
    #print(df.head(6).max())
    
    # Date Visualization
    # most mentioned picks    
    squarify.plot(sizes=times, label=top, alpha=.7 )
    plt.axis('off')
    #plt.title(f"{picks} most mentioned picks")
    plt.title("{} most mentioned picks".format(picks))
    #plt.show()
    
    # Sentiment analysis
    df = df.astype(float)
    colors = ['red', 'springgreen', 'forestgreen', 'coral']
    #df.plot(kind = 'bar', color=colors, title=f"Sentiment analysis of top {picks_ayz} picks:")
    #df.plot(kind = 'bar', color=colors, title="Sentiment analysis of top {} picks:".format(picks_ayz))
    #plt.show()

    uselessvariable1 = 'this is a useless variable to force-hide show plt.show() above when minimizing this function'

# OK
def print_logs2(symbols, scores):
    '''*****************************************************************************
    # Info logs for console program - additional info, optional
    *****************************************************************************'''
    if isPrint_logs == True:
        print("print1.1: ", symbols, "n\\") #aka tickers, mention count, dict pair of tickers and mentions
        print("print2: ", scores)
    endingvar = None

# JUST ADDED
def create_missingtables_and_clearparenttable(outputname_userinput):

    '''*****************************************************************************
    ### 0 - check if db/tables exist
    ### 1 - create db/tables (ones that are missing)
    *****************************************************************************'''
    exists_database, exists_parenttable, exists_childtable = check_exists_3tables(outputname_userinput)

    print('\ncreate_missingtables_and_clearparenttable()')
    print(f"exists_database={exists_database} | exists_parenttable={exists_parenttable} | exists_childtable={exists_childtable}")


    query_db = f"CREATE DATABASE {db_name1}"
    query_parent = f"CREATE TABLE {db_name1}.{outputname_userinput}parent (parenttable_id INT UNIQUE, subreddit_count INT, upvote_ratio DECIMAL(16, 1), ups INT, limit_reddit INT, upvotes INT, picks INT, picks_ayz INT, seconds_took DECIMAL(16, 1), comments_analyzed INT, datetime DATETIME, tickers_found INT, tickers_rsa INT, min_market_cap DECIMAL(16, 2), max_market_cap DECIMAL(16, 2));"
    query_child = f"CREATE TABLE {db_name1}.{outputname_userinput}child (ticker_id INT, symbol TEXT, mentions INT, market_cap DECIMAL(16,2), latest_price DECIMAL(16,2), change_percent DECIMAL(16,2), pe_ratio DECIMAL(16,2), company_name TEXT, datetime DATETIME, parenttable_id INT);"

    #xxx 1 = tested/ok
    if exists_database == False and exists_parenttable == False and exists_childtable == False:
        #step 1: create the database, parent, and child table (3 things) = ok
        cursor.execute(query_db)
        cursor.execute(query_parent)
        cursor.execute(query_child)
        print('xxx -> 000')

    #0xx 2 = tested/ok
    if exists_database == True and exists_parenttable == False and exists_childtable == False:
        #step 1: create parent and child table (2 things) = ok
        cursor.execute(query_parent)
        cursor.execute(query_child)
        print('0xx -> 000')

    #0x0 2 = tested/ok
    if exists_database == True and exists_parenttable == False and exists_childtable == True:
        #step 1: create parent table (1 thing) = ok
        cursor.execute(query_parent)
        print('0x0 -> 000')
        
    #00x 3 = tested/ok, should replace clear parent table part with mirror_outputs()
    if exists_database == True and exists_parenttable == True and exists_childtable == False:
        #step 1: clear parent table, create child table (2 things) = ok
        query_clearparenttable = f"DELETE FROM {db_name1}.{outputname_userinput}parent;"
        cursor.execute(query_clearparenttable)
        cursor.execute(query_child)
        print('00x -> 000')
        
    #000 3 = tested/ok
    if exists_database == True and exists_parenttable == True and exists_childtable == True:
        print('000 -> 000')

# JUST ADDED
def setup_foreign_key_and_after_delete_trigger(outputname_userinput):
    '''*****************************************************************************
    ### 0 - check if db, parent and child tables exist
    ### 1 - create fk/triggers
    *****************************************************************************'''
    exists_database, exists_parenttable, exists_childtable = check_exists_3tables(outputname_userinput)

    print('\nsetup_foreign_key_and_after_delete_trigger()')
    print(f"exists_database={exists_database} | exists_parenttable={exists_parenttable} | exists_childtable={exists_childtable}")

    #000 = testing
    if exists_database == True and exists_parenttable == True and exists_childtable == True:
        # add foreign key
        sql = f'ALTER TABLE {db_name1}.{outputname_userinput}child ADD CONSTRAINT fk_{outputname_userinput} FOREIGN KEY (parenttable_id) REFERENCES {db_name1}.{outputname_userinput}parent (parenttable_id) ON DELETE CASCADE;'
        try:
            cursor.execute(sql)
            print("added foreign key fk_a1")
        except Exception as e:
            print(e)


        # add trigger (after delete)
        sql = '''
        CREATE TRIGGER {0}.trigger_{1}
        AFTER DELETE ON {3}
        FOR EACH ROW
        begin
            DELETE FROM {2} p
            WHERE p.parenttable_id = OLD.parenttable_id
            AND
            (  SELECT COUNT(CASE WHEN {3}.parenttable_id = OLD.parenttable_id THEN 1 END) FROM {3}  ) = 0;
        end;
        '''.format(f"{db_name1}", f"trigger_{outputname_userinput}", f"{db_name1}.{outputname_userinput}parent", f"{db_name1}.{outputname_userinput}child")
        # print(sql)
        try:
            cursor.execute(sql)
            print("added trigger (after delete)")
        except Exception as e:
            print(e)


# OLD
def deleteandrename_existingoutputfiles_csv_and_sql(storagetype, list_existingoutputfiles1, max_output_amount, outputname_userinput):
    '''*****************************************************************************
    # Manage result files for proper numbering and up-to-date content
    #1 Delete first excessive result files (if result files exceed maximum allowed) = ok
    #2 Adjust other result files' numbers (ex: 2-10 to 1-9.. up to max_output_amount) = ok
    *****************************************************************************'''
    # log
    if storagetype == "mysql":
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '%{outputname_userinput}%';")
        myresult = cursor.fetchall()
        previewlist_existingoutputfiles1 = [list(a.values())[0] for a in myresult]
        print('list_existingoutputfiles1 (...)'.ljust(55), previewlist_existingoutputfiles1) #log

    if storagetype == "csv":
        previewlist_existingoutputfiles1 = []    
        for a in os.listdir(path_repo_and_csvfiles):
            if a.startswith(outputname_userinput):
                previewlist_existingoutputfiles1.append(a)
        print('list_existingoutputfiles1 (...)'.ljust(55), previewlist_existingoutputfiles1) #log
    
    
    #1
    if storagetype == "mysql": 
        while True:
            if len(list_existingoutputfiles1) >= max_output_amount:           
                #delete first table - sql
                cursor.execute(f"DROP TABLE {db_name1}.{list_existingoutputfiles1[0]};")

                #reinitialize list of tables - sql
                list_existingoutputfiles1 = []
                cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '%{outputname_userinput}%';")
                myresult = cursor.fetchall()
                list_existingoutputfiles1 = [list(a.values())[0] for a in myresult]
                    
            else:
                break

    if storagetype == "csv": 
        while True:
            if len(list_existingoutputfiles1) >= max_output_amount:
                #delete first table - csv
                delete_file = path_repo_and_csvfiles + "/" + list_existingoutputfiles1[0]
                os.remove(delete_file)

                #reinitialize list of tables - csv
                list_existingoutputfiles1 = []    
                for a in os.listdir(path_repo_and_csvfiles):
                    #print('checking', a, 'with', outputname_userinput) #log
                    if a.startswith(outputname_userinput):
                        list_existingoutputfiles1.append(a)
                
            else:
                break


    #log
    if storagetype == "mysql":
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '%{outputname_userinput}%';")
        myresult = cursor.fetchall()
        previewlist_existingoutputfiles1 = [list(a.values())[0] for a in myresult]
        print('list_existingoutputfiles1 (after del excess)  '.ljust(55), previewlist_existingoutputfiles1) #log

    if storagetype == "csv":
        previewlist_existingoutputfiles1 = []    
        for a in os.listdir(path_repo_and_csvfiles):
            if a.startswith(outputname_userinput):
                previewlist_existingoutputfiles1.append(a)
        print('list_existingoutputfiles1 (after del excess)  '.ljust(55), previewlist_existingoutputfiles1) #log


     #2
    if storagetype == "mysql":
        for a in list_existingoutputfiles1:
            try:
                num_file = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
                old_filename = f"{db_name1}.{a}"

                if num_file < 10:
                    new_filename = f"{db_name1}.{outputname_userinput}00{num_file}"
                elif num_file >= 10 and num_file < 100:
                    new_filename = f"{db_name1}.{outputname_userinput}0{num_file}"
                elif num_file >= 100 and num_file < 1000:
                    new_filename = f"{db_name1}.{outputname_userinput}{num_file}"
            
                cursor.execute(f"RENAME TABLE {old_filename} TO {new_filename};")
            except:
                continue #skip FileNotFoundError (csv) or error about filename already existing (sql)
    
    if storagetype == "csv":
        for a in list_existingoutputfiles1:
            try:            
                num_file = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
                old_filename = pathlib.Path(path_repo_and_csvfiles + "/" + a)

                if num_file < 10:
                    new_filename = pathlib.Path(path_repo_and_csvfiles + "/" + outputname_userinput + '00'+str(num_file)+'.csv')
                elif num_file >= 10 and num_file < 100:
                    new_filename = pathlib.Path(path_repo_and_csvfiles + "/" + outputname_userinput + '0'+str(num_file)+'.csv')
                elif num_file >= 100 and num_file < 1000:
                    new_filename = pathlib.Path(path_repo_and_csvfiles + "/" + outputname_userinput +str(num_file)+'.csv')

                os.rename(old_filename, new_filename)
            except:
                continue #skip FileNotFoundError (csv) or error about filename already existing (sql)


    #log
    if storagetype == "mysql":
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '%{outputname_userinput}%';")
        myresult = cursor.fetchall()
        previewlist_existingoutputfiles1 = [list(a.values())[0] for a in myresult]
        print('list_existingoutputfiles1 (after num correction)'.ljust(55), previewlist_existingoutputfiles1) #log
    
    if storagetype == "csv":
        previewlist_existingoutputfiles1 = []    
        for a in os.listdir(path_repo_and_csvfiles):
            if a.startswith(outputname_userinput):
                previewlist_existingoutputfiles1.append(a)
        print('list_existingoutputfiles1 (after num correction)'.ljust(55), previewlist_existingoutputfiles1) #log

    
# JUST ADDED
def deleteandrename_existingoutputs_sql_parenttable(max_output_amount, outputname_userinput):
    print('\ndeleteandrename_existingoutputs_sql_parenttable()')

    #get list of parenttable ids
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}parent order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('start', list_existingoutputfiles1)
    
    #delete (also deletes rows from child table thru FK)
    while True:
        if len(list_existingoutputfiles1) >= max_output_amount:           
            #delete first rows - sql
            cursor.execute(f"DELETE FROM {db_name1}.{outputname_userinput}parent where parenttable_id = {list_existingoutputfiles1[0]};")

            #reinitialize list of parenttable ids
            list_existingoutputfiles1 = []
            sql = f"select parenttable_id from {db_name1}.{outputname_userinput}parent order by parenttable_id ASC;"
            cursor.execute(sql)
            result = cursor.fetchall()
            # pprint.pprint(result)
            #turn into list
            list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
            # remove duplicates
            list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))            
        else:
            break
        
    print('trimmed', list_existingoutputfiles1)

    #rename
    cursor.execute('SET FOREIGN_KEY_CHECKS=0;') #disable (only when updating parent table's rows (not needed when deleting))
    for a in list_existingoutputfiles1:
        new_parenttable_id = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
        #old_parenttable_id  = a
        sql = f"UPDATE {db_name1}.{outputname_userinput}parent SET parenttable_id = {new_parenttable_id} where parenttable_id = {a};"
        cursor.execute(sql)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1;') #re-enable (only when updating parent table's rows (not needed when deleting))
    

    #reinitialize list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}parent order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('renamed', list_existingoutputfiles1)

# JUST ADDED
def deleteandrename_existingoutputs_sql_childtable(max_output_amount, outputname_userinput):
    print('\ndeleteandrename_existingoutputs_sql_childtable()')

    #get list of parenttable ids
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('start', list_existingoutputfiles1)

    #delete, (already deleted by parent table thru FK)
    while True:
        if len(list_existingoutputfiles1) >= max_output_amount:           
            #delete first rows - sql
            cursor.execute(f"DELETE FROM {db_name1}.{outputname_userinput}child where parenttable_id = {list_existingoutputfiles1[0]};")

            #reinitialize list of parenttable ids
            list_existingoutputfiles1 = []
            sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
            cursor.execute(sql)
            result = cursor.fetchall()
            # pprint.pprint(result)
            # turn into list
            list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
            # remove duplicates
            list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))                        
        else:
            break
    
    print('trimmed', list_existingoutputfiles1, '(already trimmed using FK constraint, no change)')

    #rename
    for a in list_existingoutputfiles1:
        new_parenttable_id = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
        #old_parenttable_id = a
        sql = f"UPDATE {db_name1}.{outputname_userinput}child SET parenttable_id = {new_parenttable_id} where parenttable_id = {a};"
        cursor.execute(sql)
    

    #reinitialize list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('renamed', list_existingoutputfiles1)

# OLD
def reformatandaddinfoto_symbolsdict(symbols):
    #add function that adds details for list of found symbols


    #reformat symbols dict
    for k,v in symbols.items():
        symbols[k] = {"mentions": v}

    #updat symbols dict (add info like marketCap, latestPrice)
    for k,v in symbols.items():

        time.sleep(0.4)

        #url = 'https://cloud.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN
        url =  'https://sandbox.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN_SANDBOX
        
        r = requests.get(url)
        # r = requests.post(url)
        # print(r.status_code, r.reason)
        # print('##1')
        # print(r)

        try:
            j = r.json()
            # print(j)

            try:            
                j_val = j["marketCap"]
                j_val = "$%.2f" % (j_val/1000000000) + "B" #{symbol: $20.00B}
                symbols[k].update({"marketCap": j_val})
            except:
                # dict_symbolmc[str(k)] = 'None/possible crypto'
                symbols[k].update({"marketCap": "NA/crypto"})

            try:
                j_val = j["latestPrice"]
                j_val = "$%.2f" % (j_val) #{symbol: $20.00}
                symbols[k].update({"latestPrice": j_val})
            except:
                symbols[k].update({"latestPrice": "NA/crypto"})

            try:
                j_val = j["changePercent"]
                j_val = "%.2f" % (j_val*100) + "%" #{symbol: 0.02%}
                symbols[k].update({"changePercent": j_val})
            except:
                symbols[k].update({"changePercent": "NA/crypto"})

            try:
                j_val = j["companyName"]
                symbols[k].update({"companyName": j_val})
            except:
                symbols[k].update({"companyName": "NA/crypto"})

            try:
                j_val = j["peRatio"]
                if j_val == "" or j_val == None: j_val = "NA"
                symbols[k].update({"peRatio": j_val})
                
            except:
                symbols[k].update({"peRatio": "NA/crypto"})

        except Exception as e:
            print(e, '--', k, r.reason)
            continue #try to bypass json.decoder error


    # pprint.pprint(symbols)
    
    # return symbols

    endingvar = None

#gives raw int, instead of string number with $ or %
def reformatandaddinfoto_symbolsdict2(symbols, marketcap_min, marketcap_max):
    #shorten 
    
    
    
    # #delete symbols based on marketcap (probably better after RSA because the symbol list is now 300-ish, instead of 11,000)
    print("\nreformatandaddinfoto_symbolsdict2()")

    list_removesymbols = []
    for k in symbols.keys():
        time.sleep(0.4)
        url =  'https://sandbox.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN_SANDBOX

        r = requests.get(url)
        # r = requests.post(url)
        # print(r.status_code, r.reason)
        # print('##2')
        # print(r)

        try:
            j = r.json()
            j_val = j["marketCap"]

            if j_val < marketcap_min or j_val > marketcap_max:
                if j_val != 0:
                    list_removesymbols.append(k)
        except Exception as e:
            print(e, k, j_val)
            continue #try avoid json error

    for i in list_removesymbols: 
        del symbols[i]
    print("removed symbols w/ >" + str(marketcap_max))
    print("list_removesymbols", list_removesymbols)    
    print("symbols:", symbols)

    #reformat symbols dict
    for k,v in symbols.items():
        symbols[k] = {"mentions": v}

    
    #update symbols dict (add info like marketCap, latestPrice) or (delete symbols based on marketCap)
    count_Null = 0
    for k,v in symbols.items():
        time.sleep(0.4)

        #url = 'https://cloud.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN
        url =  'https://sandbox.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN_SANDBOX
        
        r = requests.get(url)
        # r = requests.post(url)
        # print(r.status_code, r.reason)
        # print('##3')
        # print(r)

        try:
            j = r.json()
            # print(j)

            for a in ["marketCap", "latestPrice", "changePercent", "companyName", "peRatio"]:
                j_val = j[a]

                # if j_val == None or j_val == 0: 
                if j_val == None: 
                    # print('note: j_val == ""/None: ', j_val, type(j_val))
                    symbols[k].update({a: NULL})
                    count_Null += 1
                    continue
                
                if a == "changePercent":
                    j_val *= 100

                # if a == "marketCap" and j_val > 1000000000 and j_val != 0:
                #     print("deleted ", k, symbols[k], j_val)
                #     del symbols[k]
                #     break
                
                symbols[k].update({a: j_val})
                # print('note: j_val == : ', j_val, type(j_val))

        except Exception as e:
            print(e, '--', k, r.reason)

            for a in ["marketCap", "latestPrice", "changePercent", "companyName", "peRatio"]:
                symbols[k].update({a: NULL})

            continue #try to bypass json.decoder error
    print("NULL count: " + str(count_Null))

    # pprint.pprint(symbols)
    # return symbols

    endingvar = None

# OLD
def add_newoutputfile_csv_and_sql_empty(storagetype, outputname_generated, dt_string):
    '''*****************************************************************************
    #1 Create new output file, using outputname_generated
    #2 Insert result and additional info
    *****************************************************************************'''
    if storagetype == "mysql":
        # #1
        cursor.execute(f"CREATE TABLE {db_name1}.{outputname_generated} (tickerId INT, symbol TEXT, mentions INT, marketCap DECIMAL(16,2), latestPrice DECIMAL(16,2), changePercent DECIMAL(16,2), peRatio DECIMAL(16,2), companyName TEXT, tableId INT, PRIMARY KEY (tickerId));")

    
    if storagetype == "csv":
        #1
        if write_empty_newoutputfile == True:
            with open(outputname_generated, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date and time: ' + dt_string])
                writer.writerow(['Empty file'])

# OLD
def add_newoutputfile_csv_and_sql(storagetype, outputname_generated, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols):
    '''*****************************************************************************
    #1 Create new output file, using outputname_generated
    #2 Insert result and additional info
    *****************************************************************************'''
    if storagetype == "mysql":
        # #1
        # cursor.execute(f"CREATE TABLE {db_name1}.{outputname_generated} (Number INT, Symbols TEXT, Mentions INT, marketCap TEXT, latestPric TEXT, changePerc TEXT, peRatio TEXT, companyNam TEXT, PRIMARY KEY (Number));")
        # #1 - improved 
        cursor.execute(f"CREATE TABLE {db_name1}.{outputname_generated} (Analysis_Id INT, Symbols TEXT, Mentions INT, marketCap DECIMAL(16,2), latestPrice DECIMAL(16,2), changePerc DECIMAL(16,2), peRatio DECIMAL(16,2), companyNam TEXT, Table_Id INT, PRIMARY KEY (Analysis_Id));")


        #2
        info_tickernumber = 1
        for k,v in symbols.items():
            coldata_00 = '%-10s' % info_tickernumber
            coldata_01 = "%-10s" % k
            coldata_02 = "%10s" % v.get('mentions')
            # coldata_03 = "%10s" % senti.get('neg')
            # coldata_04 = "%10s" % senti.get('neu')
            # coldata_05 = "%10s" % senti.get('pos')
            # coldata_06 = "%10s" % senti.get('compound')
            coldata_07 = "%10s" % v.get('marketCap')
            coldata_08 = "%10s" % v.get('latestPrice')
            coldata_09 = "%10s" % v.get('changePercent')
            coldata_10 = "%10s" % v.get('peRatio')
            coldata_11 = "%10s" % v.get('companyName')

            cursor.execute(f"INSERT INTO {db_name1}.{outputname_generated} (Number, Symbols, Mentions, marketCap, latestPric, changePerc, peRatio, companyNam) VALUES ('{coldata_00}', '{coldata_01}', '{coldata_02}', '{coldata_07}', '{coldata_08}', '{coldata_09}', '{coldata_10}', '{coldata_11}');" )

            info_tickernumber += 1
        connection.commit()
    
    
    if storagetype == "csv":
        #1 and 2 (should try separating into 1 and 2)
        with open(outputname_generated, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(['Date and time: ' + dt_string])
            writer.writerow([info_subcount])
            writer.writerow([info_marketCap_limit])
            writer.writerow([info_parameters])
            writer.writerow([info_ittookxseconds])
            writer.writerow(['number of tickers: ' + str(len(symbols))])
            writer.writerow([])

            maxlength_string = 10
            col_00 = '%-10s' % 'Number'[:maxlength_string]
            col_01 = "%-10s" % 'Symbols'[:maxlength_string]
            col_02 = "%10s" % 'Mentions'[:maxlength_string]
            # col_03 = "%10s" % 'Bearish'[:maxlength_string]
            # col_04 = "%10s" % 'Neutral'[:maxlength_string]
            # col_05 = "%10s" % 'Bullish'[:maxlength_string]
            # col_06 = "%10s" % 'Total/Comp'[:maxlength_string]
            col_07 = "%10s" % 'marketCap'[:maxlength_string]
            col_08 = "%10s" % 'latestPrice'[:maxlength_string]
            col_09 = "%10s" % 'changePercent'[:maxlength_string]
            col_10 = "%10s" % 'peRatio'[:maxlength_string]
            col_11 = "%10s" % 'companyName'[:maxlength_string]
            
            #writer.writerow([col_00,col_01,col_02,col_03,col_04,col_05,col_06,col_07,col_08,col_09,col_10,col_11])
            writer.writerow([col_00,col_01,col_02,
                            col_07,col_08,col_09,col_10,col_11])
            

            info_tickernumber = 1
            for k,v in symbols.items():
                try:
                    coldata_00 = '%-10s' % info_tickernumber
                    coldata_01 = "%-10s" % k
                    coldata_02 = "%10s" % v.get('mentions')
                    # coldata_03 = "%10s" % senti.get('neg')
                    # coldata_04 = "%10s" % senti.get('neu')
                    # coldata_05 = "%10s" % senti.get('pos')
                    # coldata_06 = "%10s" % senti.get('compound')
                    coldata_07 = "%10s" % v.get('marketCap')
                    coldata_08 = "%10s" % v.get('latestPrice')
                    coldata_09 = "%10s" % v.get('changePercent')
                    coldata_10 = "%10s" % v.get('peRatio')
                    coldata_11 = "%10s" % v.get('companyName')

                    writer.writerow([coldata_00, coldata_01, coldata_02,
                                    coldata_07, coldata_08, coldata_09, coldata_10, coldata_11])

                    info_tickernumber += 1

                except AttributeError:
                    #colx_00 = '%-10s' % info_tickernumber
                    #k_ = "%-10s" % k
                    #v_ = "%10s" % v
                    #neg_ = "%10s" % 'X'
                    #neu_ = "%10s" % 'X'
                    #pos_ = "%10s" % 'X'
                    #compound_ = "%10s" % 'X'
                    #writer.writerow([colx_00, k_, v_, neg_, neu_, pos_, compound_,mc_, price_, pctchange_, name_])
                    #writer.writerow([colx_00, k_, v_,mc_, price_, pctchange_, name_])
                    continue

# OLD
def add_newoutputfile_csv_and_sql2(new_ref_number, storagetype, outputname_generated, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols):
    '''*****************************************************************************
    #1 Create new output file, using outputname_generated
    #2 Insert result and additional info
    *****************************************************************************'''
    if storagetype == "mysql":
        # #1
        cursor.execute(f"CREATE TABLE {db_name1}.{outputname_generated} (tickerId INT, symbol TEXT, mentions INT, marketCap DECIMAL(16,2), latestPrice DECIMAL(16,2), changePercent DECIMAL(16,2), peRatio DECIMAL(16,2), companyName TEXT, tableId INT, PRIMARY KEY (tickerId));")

        #2
        info_tickernumber = 1
        for k,v in symbols.items():
            coldata_00 = info_tickernumber
            coldata_01 =  "'%s'" % k
            if coldata_01 == "'NULL'": coldata_01 = "NULL"
            coldata_02 = v.get('mentions')
            # coldata_03 = senti.get('neg')
            # coldata_04 = senti.get('neu')
            # coldata_05 = senti.get('pos')
            # coldata_06 = senti.get('compound')
            coldata_07 = v.get('marketCap')
            coldata_08 = v.get('latestPrice')
            coldata_09 = v.get('changePercent')
            coldata_10 = v.get('peRatio')
            coldata_11 = "'%s'" % v.get('companyName')
            if coldata_11 == "'NULL'": coldata_11 = "NULL"
            coldata_12 = new_ref_number

            

            # don't use f string because it can't put 'NULL' as NULL, use % ()
            query1="INSERT INTO %s (tickerId, symbol, mentions, marketCap, latestPrice, changePercent, peRatio, companyName, tableId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            query1 = query1 % (f"{db_name1}.{outputname_generated}", coldata_00, coldata_01, coldata_02, 
            coldata_07, coldata_08, coldata_09, coldata_10, coldata_11, coldata_12)
            try: cursor.execute(query1)
            except: print("error:",query1)

            info_tickernumber += 1
        connection.commit()
    
    
    if storagetype == "csv":
        #1 and 2 (should try separating into 1 and 2)
        with open(outputname_generated, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(['Date and time: ' + dt_string])
            writer.writerow([info_subcount])
            writer.writerow([info_marketCap_limit])
            writer.writerow([info_parameters])
            writer.writerow([info_ittookxseconds])
            writer.writerow(['number of tickers: ' + str(len(symbols))])
            writer.writerow([])

            maxlength_string = 10
            col_00 = '%-10s' % 'Number'[:maxlength_string]
            col_01 = "%-10s" % 'Symbols'[:maxlength_string]
            col_02 = "%10s" % 'Mentions'[:maxlength_string]
            # col_03 = "%10s" % 'Bearish'[:maxlength_string]
            # col_04 = "%10s" % 'Neutral'[:maxlength_string]
            # col_05 = "%10s" % 'Bullish'[:maxlength_string]
            # col_06 = "%10s" % 'Total/Comp'[:maxlength_string]
            col_07 = "%10s" % 'marketCap'[:maxlength_string]
            col_08 = "%10s" % 'latestPrice'[:maxlength_string]
            col_09 = "%10s" % 'changePercent'[:maxlength_string]
            col_10 = "%10s" % 'peRatio'[:maxlength_string]
            col_11 = "%10s" % 'companyName'[:maxlength_string]
            
            #writer.writerow([col_00,col_01,col_02,col_03,col_04,col_05,col_06,col_07,col_08,col_09,col_10,col_11])
            writer.writerow([col_00,col_01,col_02,
                            col_07,col_08,col_09,col_10,col_11])
            

            info_tickernumber = 1
            for k,v in symbols.items():
                try:
                    coldata_00 = '%-10s' % info_tickernumber
                    coldata_01 = "%-10s" % k
                    coldata_02 = "%10s" % v.get('mentions')
                    # coldata_03 = "%10s" % senti.get('neg')
                    # coldata_04 = "%10s" % senti.get('neu')
                    # coldata_05 = "%10s" % senti.get('pos')
                    # coldata_06 = "%10s" % senti.get('compound')
                    coldata_07 = "%10s" % v.get('marketCap')
                    coldata_08 = "%10s" % v.get('latestPrice')
                    coldata_09 = "%10s" % v.get('changePercent')
                    coldata_10 = "%10s" % v.get('peRatio')
                    coldata_11 = "%10s" % v.get('companyName')

                    writer.writerow([coldata_00, coldata_01, coldata_02,
                                    coldata_07, coldata_08, coldata_09, coldata_10, coldata_11])

                    info_tickernumber += 1

                except AttributeError:
                    #colx_00 = '%-10s' % info_tickernumber
                    #k_ = "%-10s" % k
                    #v_ = "%10s" % v
                    #neg_ = "%10s" % 'X'
                    #neu_ = "%10s" % 'X'
                    #pos_ = "%10s" % 'X'
                    #compound_ = "%10s" % 'X'
                    #writer.writerow([colx_00, k_, v_, neg_, neu_, pos_, compound_,mc_, price_, pctchange_, name_])
                    #writer.writerow([colx_00, k_, v_,mc_, price_, pctchange_, name_])
                    continue

def add_newoutputfile_parenttable_empty(new_ref_number, outputname_userinput, time1_rsafinished):
    print("\nadd_newoutputfile_parenttable()")
    print(db_name1, new_ref_number, outputname_userinput)
    sql = f"INSERT INTO {db_name1}.{outputname_userinput}parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, tickers_rsa, min_market_cap, max_market_cap) VALUES ({new_ref_number}, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, '{time1_rsafinished}', 11796, 350, 1000, 4000000000);"
    cursor.execute(sql)
    connection.commit()

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
    print('end', list_existingoutputfiles1)

# JUST ADDED
def add_newoutputfile_childtable_empty(new_ref_number, outputname_userinput, time1_rsafinished):
    print("\add_newoutputfile_childtable_empty()")

    query1="INSERT INTO %schild (ticker_id, symbol, mentions, market_cap, latest_price, change_percent, pe_ratio, company_name, datetime, parenttable_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s', %s)"
    query1 = query1 % (f"{db_name1}.{outputname_userinput}", 1, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", time1_rsafinished, new_ref_number)
    cursor.execute(query1)
    connection.commit()

    #preview list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('end', list_existingoutputfiles1)


# JUST ADDED
def add_newoutputfile_parenttable(outputname_userinput, new_ref_number, subreddit_count, upvoteRatio, ups, limit, upvotes, picks, picks_ayz, seconds_took, c_analyzed, time1_rsafinished, us, symbols, marketcap_min, marketcap_max):
    print("\nadd_newoutputfile_parenttable()")

    sql = f"INSERT INTO {db_name1}.{outputname_userinput}parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, tickers_rsa, min_market_cap, max_market_cap) VALUES ({new_ref_number}, {subreddit_count}, {upvoteRatio}, {ups}, {limit}, {upvotes}, {picks}, {picks_ayz}, {seconds_took}, {c_analyzed}, '{time1_rsafinished}', {len(us)}, {len(symbols)}, {marketcap_min}, {marketcap_max});"
    
    cursor.execute(sql)
    connection.commit()

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
    print('end', list_existingoutputfiles1)

# JUST ADDED
def add_newoutputfile_childtable(new_ref_number, outputname_userinput, symbols, time1_rsafinished):
    print("\nadd_newoutputfile_childtable()")

    info_tickernumber = 1
    for k,v in symbols.items():
        coldata_00 = info_tickernumber
        coldata_01 =  "'%s'" % k
        if coldata_01 == "'NULL'": coldata_01 = "NULL"
        coldata_02 = v.get('mentions')
        # coldata_03 = senti.get('neg')
        # coldata_04 = senti.get('neu')
        # coldata_05 = senti.get('pos')
        # coldata_06 = senti.get('compound')
        coldata_07 = v.get('marketCap')
        coldata_08 = v.get('latestPrice')
        coldata_09 = v.get('changePercent')
        coldata_10 = v.get('peRatio')
        coldata_11 = "'%s'" % v.get('companyName')
        if coldata_11 == "'NULL'": coldata_11 = "NULL"
        # time1_rsafinished = "'%s'" % time1_rsafinished
        coldata_12 = new_ref_number


        # don't use f string because it can't put 'NULL' as NULL, use % ()
        query1="INSERT INTO %schild (ticker_id, symbol, mentions, market_cap, latest_price, change_percent, pe_ratio, company_name, datetime, parenttable_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '%s', %s)"
        query1 = query1 % (f"{db_name1}.{outputname_userinput}", coldata_00, coldata_01, coldata_02, 
        coldata_07, coldata_08, coldata_09, coldata_10, coldata_11, time1_rsafinished, coldata_12)
        try: cursor.execute(query1)
        except Exception as e: print(e, "error:",query1)

        info_tickernumber += 1
    connection.commit()

    #preview list of parenttable ids
    list_existingoutputfiles1 = []
    sql = f"select parenttable_id from {db_name1}.{outputname_userinput}child order by parenttable_id ASC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    # pprint.pprint(result)
    # turn into list
    list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
    # remove duplicates
    list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
    print('end', list_existingoutputfiles1)

#revise this
def print_logs3(outputname_userinput, outputname_generated):
    print()

    if storagetype == "mysql":
        cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name1}' AND table_name like '%{outputname_userinput}%';")
        myresult = cursor.fetchall()
        previewlist_existingoutputfiles1 = [list(a.values())[0] for a in myresult]
        print('existing sql tables (parent/child)', previewlist_existingoutputfiles1) #log

    if storagetype == "csv":
        previewlist_existingoutputfiles1 = []    
        for a in os.listdir(path_repo_and_csvfiles):
            if a.startswith(outputname_userinput):
                previewlist_existingoutputfiles1.append(a)
        print('existing csv tables', previewlist_existingoutputfiles1) #log

    dt_string = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
    print("Date and Time: " + dt_string + " (End main)")
    print('Created and wrote ' + outputname_generated)
    print()



def main(input, outputname_userinput, parameter_subs, marketcap_min, marketcap_max):
    '''*****************************************************************************
    # refresh/reestablish connection to mysql database = ?
    # prepare variables - (for deleting/renaming existing output files/adding new output file) - preview only
    # close connection
    *****************************************************************************'''
    if storagetype == "mysql":
        connection, cursor = connect_to_mysql()

        #one table version
        new_ref_number = prepare_variables1_sql_parentandchildtables(outputname_userinput, max_output_amount)
        outputname_generated = outputname_userinput 
        print("PREVIEW ONLY")

        cursor.close()
        connection.close()

    #if storagetype == "csv"
    #traditional 
    # outputname_generated, list_existingoutputfiles1, new_ref_number = prepare_variables1_csv_and_sql(storagetype, outputname_userinput, max_output_amount)
    
    

    '''*****************************************************************************
    #1 get list of subreddits (from csv file) - (for Reddit Sentinment Analysis)
    *****************************************************************************'''
    subs = getlist_subreddits(parameter_subs)

    '''*****************************************************************************
    #2 get list of tickers and detailed info from an api - (for Reddit Sentinment Analysis)
    *****************************************************************************'''
    # us = getlist_nasdaq_csvfile(input)


    # #PROBLEM_2: CAUSES MEMORY ISSUE ON AWS..
    # us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_nasdaq_api(marketcap_min, marketcap_max) 


    # #TEMPORARY SOLUTION 1
    #us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_from_textfile() 
    us = getlist_from_textfile()
    # print("us", us)

    # #TEMPORARY SOLUTION 2
    #us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_nasdaq_api_chunk(marketcap_min, marketcap_max)  

    
    # #TEMPORARY SOLUTION 3 (abandoned)
    #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10"
    #download_file_separate(url)    

    '''*****************************************************************************
    # prepare additional-info variables - (put additional-info into new output file)
    # print logs
    *****************************************************************************'''
    dt_string, info_subcount, info_marketCap_limit, subreddit_count = prepare_variables2_additional_info(subs, marketcap_max)
    

    print_logs1(dt_string, outputname_generated, info_subcount, info_marketCap_limit, us) #only for csv files
    

    # sys.exit("Forced exit!")



    '''*****************************************************************************
    # Reddit Sentiment Analysis
    *****************************************************************************'''
    if write_empty_newoutputfile == False:
        start_time = time.time()

        #if write_empty_newoutputfile == False:
        # open reddit client
        reddit = praw.Reddit(
            user_agent=os.environ.get('reddit_user_agent'), 
            client_id=os.environ.get('reddit_client_id'), 
            client_secret=os.environ.get('reddit_client_secret'),
            username=os.environ.get('reddit_username'), 
            password=os.environ.get('reddit_password')
        )

        #not working..
        # reddit = praw.Reddit(
        #     user_agent, 
        #     client_id, 
        #     client_secret, 
        #     username, 
        #     password
        # )
        
        # posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz, info_parameters = data_extractor(reddit, subs, us)
        posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz, info_parameters, upvoteRatio, ups, limit, upvotes = data_extractor(reddit, subs, us)
        print('data_extractor finished')

        # symbols, times, top, info_ittookxseconds = print_helper(tickers, picks, c_analyzed, posts, subs, titles, time, start_time)
        symbols, times, top, info_ittookxseconds, seconds_took = print_helper(tickers, picks, c_analyzed, posts, subs, titles, time, start_time)
        print('print_helper finished')

        #PROBLEM_3: Seems to not work on AWS's due to excessive memory usage...
        if use_sentiment_analysis_and_visualization == True:
            scores = sentiment_analysis(picks_ayz, a_comments, symbols, us)
            print('sentiment_analysis finished') 

            visualization(picks_ayz, scores, picks, times, top)
            print('visualization finished') 

            print_logs2(symbols, scores)

    time1_rsafinished = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(time1_rsafinished, type(time1_rsafinished))

    '''*****************************************************************************
    # refresh/reestablish connection to mysql database = ?
    *****************************************************************************'''
    if storagetype == "mysql":
        connection, cursor = connect_to_mysql()


    '''*****************************************************************************
    # create missing tables if needed
    # setup FK and trigger (after-delete)
    *****************************************************************************'''
    
    create_missingtables_and_clearparenttable(outputname_userinput)
    setup_foreign_key_and_after_delete_trigger(outputname_userinput)


    '''*****************************************************************************
    # update output file
    *****************************************************************************'''
    # might be causing MEMORYERROR - probably not
    # deleteandrename_existingoutputfiles_csv_and_sql(storagetype, list_existingoutputfiles1, max_output_amount, outputname_userinput)

    if storagetype == "mysql":
        #one table version
        new_ref_number = prepare_variables1_sql_parentandchildtables(outputname_userinput, max_output_amount)
        outputname_generated = outputname_userinput 
        print("ACTUAL REF NUMBER")
        
        deleteandrename_existingoutputs_sql_parenttable(max_output_amount, outputname_userinput)
        deleteandrename_existingoutputs_sql_childtable(max_output_amount, outputname_userinput)


    '''*****************************************************************************
    # fix/update symbol dictionary with more info
    *****************************************************************************'''
    if write_empty_newoutputfile == False:
        #if write_empty_newoutputfile == False:
        # might be causing MEMORYERROR - ?
        # dict_symbolmc = {'AAPL': '$3035.xB', 'MSFT': '$2514.xB', 'GOOG': '$1974.xB', 'GOOGL': '$1967.xB', 'AMZN': '$1786.xB'}
        # dict_symbolmc = {}
        # dict_symbolprice = {'AAPL': '$175.x', 'MSFT': '$334.x', 'GOOG': '$2974.x', 'GOOGL': '$2963.x', 'AMZN': '$3523.x'}
        # dict_symbolpctchange = {'AAPL': '2.x%', 'MSFT': '0.x%', 'GOOG': '0.x%', 'GOOGL': '0.x%', 'AMZN': '-0.x%'}
        # dict_name = {'AAPL': ' Apple Inc. Common Stock', 'MSFT': ' Microsoft Corporation Common Stock', 'GOOG': ' Alphabet Inc. Class C Capital Stock', 'GOOGL': ' Alphabet Inc. Class A Common Stock', 'AMZN': ' Amazon.com, Inc. Common Stock'}    
        # add_newoutputfile_csv_old(outputname_generated, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name)

        # #OR
        # might be causing MEMORYERROR - testing, probbably not
        reformatandaddinfoto_symbolsdict2(symbols, marketcap_min, marketcap_max)


        

    '''*****************************************************************************
    # add new output file
    *****************************************************************************'''
    # if write_empty_newoutputfile == False:
    #     add_newoutputfile_csv_and_sql2(new_ref_number, storagetype, outputname_generated, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols)
    
    # if write_empty_newoutputfile == True:
    #     add_newoutputfile_csv_and_sql_empty(storagetype, outputname_generated, dt_string)
    if storagetype == "mysql":
        if write_empty_newoutputfile == True:
            add_newoutputfile_parenttable_empty(new_ref_number, outputname_userinput, time1_rsafinished)
            add_newoutputfile_childtable_empty(new_ref_number, outputname_userinput, time1_rsafinished)

        if write_empty_newoutputfile == False:
            add_newoutputfile_parenttable(outputname_userinput, new_ref_number, subreddit_count, upvoteRatio, ups, limit, upvotes, picks, picks_ayz, seconds_took, c_analyzed, time1_rsafinished, us, symbols, marketcap_min, marketcap_max)

            if symbols != {}:
                add_newoutputfile_childtable(new_ref_number, outputname_userinput, symbols, time1_rsafinished)
            elif symbols == {}:
                add_newoutputfile_childtable_empty(new_ref_number, outputname_userinput, time1_rsafinished)


    '''*****************************************************************************
    # print logs
    # close connection
    *****************************************************************************'''
    print_logs3(outputname_userinput, outputname_generated)


    if storagetype == "mysql":
        cursor.close()
        connection.close()



def run_batch_of_processes_1():
    start_time = time.time()
    
    '''*****************************************************************************
    # create separate process for each function 
    # should reinitialize those process variables if starting them multiple time (in while loop or schedule module)
    *****************************************************************************'''
    # way 1 - local machine
    # process_1 = Process(target=main, args=(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)) 
    # process_2 = Process(target=main, args=(input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3))
    # process_3 = Process(target=main, args=(input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_min0, marketcap_max4))

    # way 2  - test
    process_1 = Process(target=main, args=(input_api_nasdaq, 'result_test1_', subs_specificlist1, marketcap_min0, marketcap_max1)) 
    process_2 = Process(target=main, args=(input_api_nasdaq, 'result_test2_', subs_specificlist1, marketcap_min0, marketcap_max3))
    process_3 = Process(target=main, args=(input_api_nasdaq, 'result_test3_', subs_specificlist1, marketcap_min0, marketcap_max4))


    '''*****************************************************************************
    # starts the processes
    *****************************************************************************'''
    process_1.start(); process_2.start(); process_3.start()


    '''*****************************************************************************
    # wait till they all finish and close them
    *****************************************************************************'''
    process_1.join(); process_2.join(); process_3.join()


    print("--- %s seconds ---" % (time.time() - start_time));print()



if __name__ == '__main__':    
    '''*****************************************************************************
    # WAY 4 - run program by multiprocessing once (for aws with cron jobs i guess)
    # testing
    *****************************************************************************'''
    #run_batch_of_processes_1() ##immediate, test


    '''*****************************************************************************
    # WAY 0 - run program normally
    # Parameter: program_number
    *****************************************************************************'''
    #print("WAY 0 rsa.py used")
    
    main(input_api_nasdaq, output_filename1_RDS, subs_membercount_min1, marketcap_min0, marketcap_max1) ##stable RDS
    # main(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1) ##stable
    #main(input_api_nasdaq, output_filename1_RDS, subs_membercount_min1, marketcap_min0, marketcap_max1) ##linux/window test large
    #main(input_api_nasdaq, output_filename4_RDS, subs_specificlist1, marketcap_min0, marketcap_max4) ##linux/window test small
    #main(input_api_nasdaq, output_filename0, subs_membercount_min2, marketcap_min0, marketcap_max4) ##linux test - testing getlist_subreddits - WORKING, needs TESTING
    #main(input_api_nasdaq, output_filename0, subs_specificlist1, marketcap_min0, marketcap_max4)


    '''*****************************************************************************
    # WAY 1 - run program by schedule (old)
    # Parameter: program_number
    *****************************************************************************'''
    #####schedule.every().day.at("01:00")
    #####schedule.every().minute.at(":08").do(main, csvfile6)
    ###idea = main(input, outputname_userinput, marketcap, 0, subreddit members, etc.)
    ###idea = main(input_csvfile, savedtickers4b, subs_membercount_min1, 4,000,000,000, member counts)
    ###idea = main(input_csvfile, savedtickers200b, subs_membercount_min1, 200,000,000,000, 200,000)

    # program_number = 1
    # schedule.every().day.at("23:55").do(nltk.download, 'wordnet')

    # if program_number == 1:
    #    #program one
    #    main(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1) ##
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)
    #    schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min0, marketcap_max1)

    # if program_number == 2:
    #    #program two
    #    #main(input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    #schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    #schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
    #    #schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min0, marketcap_max3)
       
    # if program_number == 3:
    #    #program three
    #    main(input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    #schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    #schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)
    #    #schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename4, subs_specificlist1, marketcap_min0, marketcap_max4)

    # while True:
    #   schedule.run_pending()
    

    '''*****************************************************************************
    # WAY 1.1 - run program by cmd lines (for aws with cron jobs ig) (old?)
    # Parameter: program_number
    *****************************************************************************'''
    #print(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 'akak3'

    #cmd lines 1
    ####python rsa.py api.nasdaq.com result_test_ ['wallstreetbets'] 800000000 && rsa.py api.nasdaq.com result_test_ ['wallstreetbets'] 500000000 &
    ####python rsa.py api.nasdaq.com result_test_ ['wallstreetbets'] 800000000 & rsa.py api.nasdaq.com result_test_ ['wallstreetbets'] 500000000 &
    ####python rsa.py api.nasdaq.com result_test_ ['wallstreetbets'] 800000000

    #main(str(sys.argv[1]), str(sys.argv[2]), list(sys.argv[3]), int(sys.argv[4]))

    #cmd lines 2
    ####python rsa.py api.nasdaq.com result_test_ 0 15000000000 && python rsa.py api.nasdaq.com result_test_ 0 9000000000000 &
    ####python rsa.py api.nasdaq.com result_test_ 0 15000000000 & python rsa.py api.nasdaq.com result_test_ 0 9000000000000 &
    ####python rsa.py api.nasdaq.com result_test_ 0 120000000 && python rsa.py api.nasdaq.com result_test_ 0 450000000 &
    ####python rsa.py api.nasdaq.com result_test_ 0 120000000 & python rsa.py api.nasdaq.com result_test_ 0 450000000 &
    ####python rsa.py api.nasdaq.com result_test_ 0 120000000

    #main(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))   
    

    '''*****************************************************************************
    # WAY 2 - run program for n times with delay
    *****************************************************************************'''
    #result_4b_300run_
    #result_4b_1hrdelay_formoretickers_

    # print("using way 2 - run program by fixed intervals (old)")
    # for n in range(300):
    #     main(input_api_nasdaq, 'result_4b_15mindelay_formoretickers_', subs_specificlist1, marketcap_min0, marketcap_max4) ##linux/window test small (1 sub)
    #     # main(input_api_nasdaq, output_filename1_RDS, subs_membercount_min1, marketcap_min0, marketcap_max1) ##linux/window test large (64 subs)
    #     time.sleep(900)

        # subs_membercount_min1,subs_specificlist1 

    # input("Press any key to continue . . . (1) ")
    # input("Press any key to continue . . . (2) ")
    # input("Press any key to continue . . . (3) ")
    # input("Press any key to continue . . . (4) ")


    '''*****************************************************************************
    # WAY 3 - run program by schedule & multiprocessing (good for local machine.. just one click to run)
    # testing
    *****************************************************************************'''

    # schedule.every().day.at("00:00").do(run_batch_of_processes_1)
    # #schedule.every().day.at("03:00").do(run_batch_of_processes_1)
    # schedule.every().day.at("06:00").do(run_batch_of_processes_1)
    # schedule.every().day.at("09:00").do(run_batch_of_processes_1)
    # schedule.every().day.at("12:00").do(run_batch_of_processes_1)
    # #schedule.every().day.at("15:00").do(run_batch_of_processes_1)
    # schedule.every().day.at("18:00").do(run_batch_of_processes_1)
    # schedule.every().day.at("21:00").do(run_batch_of_processes_1)
    
    # # run_batch_of_processes_1() ##immediate, test

    # while True:   
    #    schedule.run_pending()

    
    endingvar = None

    
    
