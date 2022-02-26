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
#!/usr/bin/python
from data import *
import os, sys, csv, praw, requests, time, pandas as pd, string, schedule, pathlib, pprint, urllib.request, en_core_web_sm, matplotlib.pyplot as plt, squarify, ast
import emoji    # removes emojis
import re   # removes links
from multiprocessing import Process
from threading import Thread
from prawcore.exceptions import Forbidden
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet', quiet=True) #what does this do?
nltk.download('vader_lexicon', quiet=True)


# don't use, try polygon instead, try IEX cloud api instead
# import finnhub
# # Setup client
# finnhub_client = finnhub.Client(api_key="f")
# # Stock candles
# print('stock symbosl')
# print(finnhub_client.stock_symbols('US'))



'''*****************************************************************************
# variables of file paths & options & environment variables
*****************************************************************************'''
path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + '/..'))
path_csvfiles = '/csvfiles'
path_repo_and_csvfiles = str(pathlib.Path(path_repo + path_csvfiles))


isPrint_logs = True
use_sentiment_analysis_and_visualization = False


IEX_TOKEN = os.environ.get('IEX_TOKEN')
IEX_TOKEN = F'?token={IEX_TOKEN}' 


'''*****************************************************************************
# Parameters for main function
*****************************************************************************'''
input_api_nasdaq = 'api.nasdaq.com'
# input_csvfile2 = path_csvfiles + '/nasdaq_screener_1631232074452_all1.csv'

output_filename0 = 'result_test_'
output_filename1 = 'result_all_'
output_filename2 = 'result_200b_'
output_filename3 = 'result_15b_'
output_filename4 = 'result_4b_'
output_filename5 = 'result_4m_'

subs_specificlist1 = ['wallstreetbets']
subs_specificlist2 = ['Stocks', 'Bitcoin', 'Wallstreetbetsnew', 'PennyStocks', 'algotrading', 'Economics', 'investing', 'Pennystocks', 'StockMarket', 'stocks', 'Investing', 'pennystocks', 'Options', 'AlgoTrading', 'wallstreetbets', 'Cryptocurrency', 'WallStreetBets']
subs_specificlist3 = ['Finance', 'Stocks', 'Bitcoin', 'SecurityAnalysis', 'Wallstreetbetsnew', 'StocksAndTrading', 'PennystocksDD', 'PennyStocks', 'algotrading', 'babystreetbets', 'Economics', 'ASX_Bets', 'antstreetbets', 'quant', 'weedstocks', 'investing', 'Economy', 'shortinterestbets', 'thetagang', 'Pennystocks', 'InvestingRetards', 'wallstreetbet', 'wallstreetbetsoptions', 'econmonitor', 'Wallstreetwarrior', 'StockMarket', 'Dividends', 'wallstreetbets2', 'Trading', 'WSBAfterHours', 'smallstreetbets', 'retardbets', 'finance', 'InvestmentClub', 'stocks', 'IndianStreetBets', 'wallstreetsidebets', 'Stock_Picks', 'baystreetbets', 'ameisenstrassenwetten', 'wallstreetbets_', 'ISKbets', 'quantfinance', 'stonks', 'GlobalMarkets', 'Investing', 'Daytrading', 'WallStreetbetsELITE', 'RobinHoodPennyStocks', 'DayTrading', 'CanadianInvestor', 'pennystocks', 'Options', 'AlgoTrading', 'MoonBets', 'algorithmictrading', 'farialimabets', 'Wallstreetsilver', 'wallstreetbets', 'Cryptocurrency', 'UKInvesting', 'ausstocks', 'WallStreetBets', 'dividends']
subs_specificlist4 = ['Bitcoin', 'Cryptocurrency', 'DayTrading']
subs_membercount_min1 = 0
subs_membercount_min2 = 600000
subs_membercount_min3 = 1000000

marketcap_min1 = 0
marketcap_min2 = 50000000000
marketcap_max1 = 9000000000000 #all
marketcap_max2 = 200000000000
marketcap_max3 = 15000000000
marketcap_max4 = 4000000000
marketcap_max5 = 4000000

#testing line 306 #limit amount of symbols/picks printed
                  # if top_picks.index(i) >= picks: #testing
                  #     break

# # import resource #linux only
# # def memory_limit():
# #     soft, hard = resource.getrlimit(resource.RLIMIT_AS)
# #     resource.setrlimit(resource.RLIMIT_AS, (int(get_memory() * 1024 / 8), hard))
# # def get_memory():
# #     with open('/proc/meminfo', 'r') as mem:
# #         free_memory = 0
# #         for i in mem:
# #             sline = i.split()
# #             if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
# #                 free_memory += int(sline[1])
# #     return free_memory


def ftn_rsa1():
    print('ftn_rsa1() on rsa.py used')

def prepare_variables1(outputfilename_custom):
    '''*****************************************************************************
    # Preparing latest outputfilename_custom filename
    # Parameter: max_output_amount
    #1 get a list of existing saved file that contains given outputfilename_custom = ok
    #2 get len = ok
    #3 get new ref number (10 if 10 files there already, 10 if 9 there already, 9 if 8 files there already, 1 if 0, 2 if 1) = ok
    #4 get potential outputfilename_custom filename.. to be created if program finishes) = ok
    *****************************************************************************'''
    # #1
    list_savedcsvfiles = []    
    for a in os.listdir(path_repo_and_csvfiles):
        #print('checking', a, 'with', outputfilename_custom) #log
        if a.startswith(outputfilename_custom + '0') or a.startswith(outputfilename_custom + '1'):
            list_savedcsvfiles.append(a)
    #print('list_savedcsvfiles', list_savedcsvfiles) #log

    #2,3
    max_output_amount = 10
    if len(list_savedcsvfiles) >= max_output_amount-1:
        new_ref_number = max_output_amount
    else:
        new_ref_number = len(list_savedcsvfiles) + 1
    #print('new_ref_number: ', new_ref_number) #log

    #4
    if new_ref_number <= 9:
        path_newoutputfilename = path_repo_and_csvfiles + "/" + outputfilename_custom + '00' + str(new_ref_number) + '.csv'
    elif new_ref_number >= 10:
        path_newoutputfilename = path_repo_and_csvfiles + "/" + outputfilename_custom + '0' + str(new_ref_number) + '.csv'
    #print('path_newoutputfilename', path_newoutputfilename) #log

    return path_newoutputfilename, list_savedcsvfiles, max_output_amount
def prepare_variables2(subs, marketcap_max):
    dt_string = datetime.now().strftime("%m/%d/%Y %H:%M")
    info_subcount = 'Sub count: ' + str(len(subs))
    
    if marketcap_max > 2000000000000: 
        info_marketCap_limit = 'Market Cap min: >2 trillions' 
    else: 
        info_marketCap_limit = 'Market Cap min: ' + str(marketcap_max/1000000000) + ' billion(s)'

    return dt_string, info_subcount, info_marketCap_limit
def print_logs1(dt_string, input, path_newoutputfilename, info_subcount, info_marketCap_limit, us):
    if isPrint_logs == True:
        print("------------------------------------------------------")
        print("Date and Time: " + dt_string + " (Beg main)")
        print('Input: ' + input)
        print('Path outputfilename_custom: ' + path_newoutputfilename)
        print(info_subcount)
        print(info_marketCap_limit)
        print('Number of tickers found (from input): ' + str(len(us)))

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
    ups = 20       # define # of upvotes, post is considered if upvotes exceed this # #20
    limit = 1     # define the limit, comments 'replace more' limit
    upvotes = 2     # define # of upvotes, comment is consi adered if upvotes exceed this #20
    picks = 100     # define # of picks here, prints as "Top ## picks are:" 10
    picks_ayz = 100   # define # of picks for sentiment analysis 5
    

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

    return posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz, info_parameters
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
    time = (time.time() - start_time)
    
    info_ittookxseconds = "It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.".format(t=time, c=c_analyzed, p=posts, s=len(subs)) #log print
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
        #limit amount of symbols/picks printed
        if top_picks.index(i) >= picks: #testing
            break
        
        if isPrint_logs == True:
            if top_picks.index(i) < 5: #only print up to 5
                print("{}: {}".format(i,symbols[i]))
        times.append(symbols[i])
        top.append("{}: {}".format(i,symbols[i]))

    return symbols, times, top, info_ittookxseconds
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
def print_logs1_5(symbols, scores):
    '''*****************************************************************************
    # Info logs for console program - additional info, optional
    *****************************************************************************'''
    #if isPrint_logs == True:
        #print("print1.1: ", symbols, "n\\") #aka tickers, mention count, dict pair of tickers and mentions
        #print("print2: ", scores)

def update_previousoutputfilenames(list_savedcsvfiles, max_output_amount, outputfilename_custom):
    '''*****************************************************************************
    # Manage result files for proper numbering and up-to-date content
    #1 Delete first result file (if result files exceed maximum allowed)
    #2 Adjust other result files' numbers (ex: 2-10 to 1-9)
    *****************************************************************************'''

    if len(list_savedcsvfiles) >= max_output_amount:
        for a in list_savedcsvfiles:
            num_file = list_savedcsvfiles.index(a) + 1 #adjust from 0 to 1
            try:
                #delete if any
                if num_file == 1:
                    delete_file = path_repo_and_csvfiles + "/" + outputfilename_custom + '001'+'.csv'

                    os.remove(delete_file)
                    #print('deleted ' + delete_file) #log

                #rename 2-9 to 1-8
                if num_file <= 9 and num_file >= 2: 
                    old_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '00'+str(num_file)+'.csv'
                    new_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '00'+str(num_file-1)+'.csv'

                    os.rename(old_filename, new_filename)
                    #print('renamed ' + old_filename + ' to ' + new_filename) #log
            
                #rename 10 to 9
                elif num_file == 10:
                    old_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '0'+str(num_file)+'.csv'
                    new_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '00'+str(num_file-1)+'.csv'

                    os.rename(old_filename, new_filename)
                    #print('renamed ' + old_filename + ' to ' + new_filename) #log

                #rename 11-.. to 10-..
                elif num_file >= 11:
                    old_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '0'+str(num_file)+'.csv'
                    new_filename = path_repo_and_csvfiles + "/" + outputfilename_custom + '0'+str(num_file-1)+'.csv'

                    os.rename(old_filename, new_filename)
                    #print('renamed ' + old_filename + ' to ' + new_filename) #log

            except FileNotFoundError:
                continue

    elif len(list_savedcsvfiles) < max_output_amount: 
        #correct naming
    
        for a in list_savedcsvfiles:
            try:
                num_file = list_savedcsvfiles.index(a) + 1 #adjust from 0 to 1
                old_filename = pathlib.Path(path_repo_and_csvfiles + "/" + a)
                new_filename = pathlib.Path(path_repo_and_csvfiles + "/" + outputfilename_custom + '00'+str(num_file)+'.csv')
                
                os.rename(old_filename, new_filename)

            except FileNotFoundError:
                continue
def reformatandaddinfoto_symbolsdict(symbols):
    #print(symbols)
    #add function that adds details for list of found symbols


    #reformat symbols dict
    for k,v in symbols.items():
        symbols[k] = {"mentions": v}

    #updat symbols dict (add info like marketCap, latestPrice)
    for k,v in symbols.items():
        url = 'https://cloud.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN
        r = requests.get(url)
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

    # pprint.pprint(symbols)
    
    # return symbols

def add_newoutputfile_empty(path_newoutputfilename, dt_string):
    with open(path_newoutputfilename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date and time: ' + dt_string])
        writer.writerow(['Empty file'])



def add_newoutputfile_old(path_newoutputfilename, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name):
    '''*****************************************************************************
    #1 Take the latest outputfilename_custom filename
    #2 Write Reddit Sentinment Analysis result onto it
    *****************************************************************************'''
    #print('writing to ' + path_newoutputfilename) #log
    with open(path_newoutputfilename, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['Date and time: ' + dt_string])
        writer.writerow([info_subcount])
        writer.writerow([info_marketCap_limit])
        writer.writerow([info_parameters])
        writer.writerow([info_ittookxseconds])
        writer.writerow(['number of tickers: ' + str(len(symbols))])
        writer.writerow([])

        col_00 = '%-10s' % 'Number'
        col_01 = "%-10s" % 'Symbols'
        col_02 = "%10s" % 'Mentions'
        # col_03 = "%10s" % 'Bearish'
        # col_04 = "%10s" % 'Neutral'
        # col_05 = "%10s" % 'Bullish'
        # col_06 = "%10s" % 'Total/Comp'
        col_07 = "%10s" % 'MarketCap'
        col_08 = "%10s" % 'Price'
        col_09 = "%10s" % 'PctChange'
        col_10 = "%10s" % 'Name'
        col_11 = "%10s" % 'ShortFloat'
        #writer.writerow([col_00,col_01,col_02,col_03,col_04,col_05,col_06,col_07,col_08,col_09,col_10,col_11])
        writer.writerow([col_00,col_01,col_02,col_07,col_08,col_09,col_10,col_11])


        info_tickernumber = 1
        for k,v in symbols.items():
            try:
                colx_00 = '%-10s' % info_tickernumber
                k_ = "%-10s" % k
                v_ = "%10s" % v
                # senti = scores.get(k)
                # neg_ = "%10s" % senti.get('neg')
                # neu_ = "%10s" % senti.get('neu')
                # pos_ = "%10s" % senti.get('pos')
                # compound_ = "%10s" % senti.get('compound')
                mc_ = "%10s" % dict_symbolmc.get(k)
                price_ = "%10s" % dict_symbolprice.get(k)
                pctchange_ = "%10s" % dict_symbolpctchange.get(k)
                name_ = dict_name.get(k)

                #writer.writerow([colx_00, k_, v_, neg_, neu_, pos_, compound_,mc_, price_, pctchange_, name_])
                writer.writerow([colx_00, k_, v_,mc_, price_, pctchange_, name_])

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

        #csv.writer(...).writerows(my_dict.items())

def add_newoutputfile(path_newoutputfilename, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols):
    '''*****************************************************************************
    #1 Take the latest outputfilename_custom filename
    #2 Write Reddit Sentinment Analysis result onto it
    *****************************************************************************'''
    #print('writing to ' + path_newoutputfilename) #log
    with open(path_newoutputfilename, 'w', newline='') as f:
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

        #csv.writer(...).writerows(my_dict.items())
def print_logs2(path_newoutputfilename):
    dt_string = datetime.now().strftime("%m/%d/%Y %H:%M")
    print("Date and Time: " + dt_string + " (End main)")
    print('Created and wrote ' + path_newoutputfilename)
    print()


def main(input, outputfilename_custom, parameter_subs, marketcap_min, marketcap_max):
    '''*****************************************************************************
    # prepare variables - (for updating output files/adding new output file)
    *****************************************************************************'''
    path_newoutputfilename, list_savedcsvfiles, max_output_amount = prepare_variables1(outputfilename_custom)
    

    '''*****************************************************************************
    #1 get list of subreddits (from csv file) - (for Reddit Sentinment Analysis)
    *****************************************************************************'''
    #1 
    # ####way 2 - just use custom sub list
    # PROBLEM_1: CAUSES MEMORY ISSUE ON AWS unless avoiding reading/extracting a csv file - SEEMS TO WORK NOW
    subs = getlist_subreddits(parameter_subs)
    # #TEMPORARY SOLUTION:
    #subs = ['wallstreetbets']


    '''*****************************************************************************
    #2 get list of tickers and detailed info from an api - (for Reddit Sentinment Analysis)
    *****************************************************************************'''
    # us = getlist_nasdaq_csvfile(input) # or
    # #PROBLEM_2: CAUSES MEMORY ISSUE ON AWS..
    # us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_nasdaq_api(marketcap_min, marketcap_max) 
    # #TEMPORARY SOLUTION 1
    #us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_from_api_temporarysolution() 
    us = getlist_from_api_temporarysolution()
    # #TEMPORARY SOLUTION 2
    #us, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name = getlist_nasdaq_api_chunk(marketcap_min, marketcap_max)  
    # #TEMPORARY SOLUTION 3 (abandoned)
    #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10"
    #download_file_separate(url) 



    '''*****************************************************************************
    # prepare variables - (for adding content to new output file), print logs
    *****************************************************************************'''
    dt_string, info_subcount, info_marketCap_limit = prepare_variables2(subs, marketcap_max)
    print_logs1(dt_string, input, path_newoutputfilename, info_subcount, info_marketCap_limit, us)
    

    '''*****************************************************************************
    # Reddit Sentiment Analysis
    *****************************************************************************'''
    start_time = time.time()
    # reddit client
    

    reddit = praw.Reddit(
        user_agent=os.environ.get('reddit_user_agent'), 
        client_id=os.environ.get('reddit_client_id'), 
        client_secret=os.environ.get('reddit_client_secret'),
        username=os.environ.get('reddit_username'), 
        password=os.environ.get('reddit_password')
    )

    #not working??
    # reddit = praw.Reddit(
    #     user_agent, 
    #     client_id, 
    #     client_secret, 
    #     username, 
    #     password
    # )
    
    posts, c_analyzed, tickers, titles, a_comments, picks, subs, picks_ayz, info_parameters = data_extractor(reddit, subs, us); print('data_extractor finished')
    symbols, times, top, info_ittookxseconds = print_helper(tickers, picks, c_analyzed, posts, subs, titles, time, start_time); print('print_helper finished')
    #PROBLEM_3: Seems to not work on AWS's due to excessive memory usage...
    if use_sentiment_analysis_and_visualization == True:
        scores = sentiment_analysis(picks_ayz, a_comments, symbols, us); print('sentiment_analysis finished') 
        visualization(picks_ayz, scores, picks, times, top); print('visualization finished') 
        print_logs1_5(symbols, scores)


    '''*****************************************************************************
    # update output file
    *****************************************************************************'''
    # might be causing MEMORYERROR - ?
    #update_previousoutputfilenames(list_savedcsvfiles, max_output_amount, outputfilename_custom)


    '''*****************************************************************************
    # fix/update symbol dictionary with more info, add new output file
    *****************************************************************************'''
    # might be causing MEMORYERROR - ?
    # dict_symbolmc = {'AAPL': '$3035.xB', 'MSFT': '$2514.xB', 'GOOG': '$1974.xB', 'GOOGL': '$1967.xB', 'AMZN': '$1786.xB'}
    # dict_symbolmc = {}
    # dict_symbolprice = {'AAPL': '$175.x', 'MSFT': '$334.x', 'GOOG': '$2974.x', 'GOOGL': '$2963.x', 'AMZN': '$3523.x'}
    # dict_symbolpctchange = {'AAPL': '2.x%', 'MSFT': '0.x%', 'GOOG': '0.x%', 'GOOGL': '0.x%', 'AMZN': '-0.x%'}
    # dict_name = {'AAPL': ' Apple Inc. Common Stock', 'MSFT': ' Microsoft Corporation Common Stock', 'GOOG': ' Alphabet Inc. Class C Capital Stock', 'GOOGL': ' Alphabet Inc. Class A Common Stock', 'AMZN': ' Amazon.com, Inc. Common Stock'}    
    # add_newoutputfile_old(path_newoutputfilename, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols, dict_symbolmc, dict_symbolprice, dict_symbolpctchange, dict_name)

    # #OR
    # might be causing MEMORYERROR - testing, probbably not the one causing error
    reformatandaddinfoto_symbolsdict(symbols)
    print('reformatted symbols')
    for k,v in symbols.items():
        print(k,v)
    # might be causing MEMORYERROR - ?
    # add_newoutputfile(path_newoutputfilename, dt_string, info_subcount, info_marketCap_limit, info_parameters, info_ittookxseconds, symbols)

    # might be causing MEMORYERROR - ?
    #add_newoutputfile_empty(path_newoutputfilename, dt_string)


    '''*****************************************************************************
    # print logs
    *****************************************************************************'''
    print_logs2(path_newoutputfilename)


def run_batch_of_processes_1():
    #TO-DO: simplify run_batch_of.. and see if it still supports scheduling.. not important!
    start_time = time.time()

    # create separate process for each function 
    # should reinitialize those process variables if starting them multiple time (in while loop or schedule module)
    # way 1 - local machine
    process_1 = Process(target=main, args=(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min1, marketcap_max1)) 
    process_2 = Process(target=main, args=(input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_min1, marketcap_max3))
    process_3 = Process(target=main, args=(input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_min1, marketcap_max4))

    # way 2  - test
    # process_1 = Process(target=main, args=(input_api_nasdaq, 'result_test1_', subs_specificlist1, marketcap_min1, marketcap_max1)) 
    # process_2 = Process(target=main, args=(input_api_nasdaq, 'result_test2_', subs_specificlist1, marketcap_min1, marketcap_max3))
    # process_3 = Process(target=main, args=(input_api_nasdaq, 'result_test3_', subs_specificlist1, marketcap_min1, marketcap_max4))

    # starts the processes
    process_1.start(); process_2.start(); process_3.start()

    # wait till they all finish and close them
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
    main(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_min1, marketcap_max1) ##stable
    #main(input_api_nasdaq, output_filename0, subs_membercount_min1, marketcap_min1, marketcap_max1) ##linux/window test large
    #main(input_api_nasdaq, output_filename0, subs_specificlist1, marketcap_min1, marketcap_max4) ##linux/window test small
    #main(input_api_nasdaq, output_filename0, subs_membercount_min2, marketcap_min1, marketcap_max4) ##linux test - testing getlist_subreddits - WORKING, needs TESTING
    #main(input_api_nasdaq, output_filename0, subs_specificlist1, marketcap_min1, marketcap_max4)

    '''*****************************************************************************
    # WAY 0.1 - run program normally with "memory limiter" which only work in Linux
    # Parameter: program_number
    *****************************************************************************'''
    #"memory limiter"
    # memory_limit() # Limitates maximun memory usage to half
    # try:
    #     main(input_api_nasdaq, output_filename0, subs_specificlist1, marketcap_min1, marketcap_max1) ##test
    #     print('memory_limitoooo, main() finished')
    # except MemoryError:
    #     sys.stderr.write('\n\nERROR: Memory Exception\n')
    #     sys.exit(1)


    '''*****************************************************************************
    # WAY 1 - run program by schedule (old)
    # Parameter: program_number
    *****************************************************************************'''
    #####schedule.every().day.at("01:00")
    #####schedule.every().minute.at(":08").do(main, csvfile6)
    ###idea = main(input, outputfilename_custom, marketcap, 0, subreddit members, etc.)
    ###idea = main(input_csvfile, savedtickers4b, subs_membercount_min1, 4,000,000,000, member counts)
    ###idea = main(input_csvfile, savedtickers200b, subs_membercount_min1, 200,000,000,000, 200,000)

    #program_number = 1
    #schedule.every().day.at("23:55").do(nltk.download, 'wordnet')

    #if program_number == 1:
    #    #program one
    #    #main(input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1) ##
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    #schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)
    #    #schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename1, subs_membercount_min1, marketcap_max1)

    #if program_number == 2:
    #    #program two
    #    #main(input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    #schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    #schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
    #    #schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename3, subs_membercount_min1, marketcap_max3)
       
    #if program_number == 3:
    #    #program three
    #    #main(input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    schedule.every().day.at("00:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    #schedule.every().day.at("03:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    schedule.every().day.at("06:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    schedule.every().day.at("09:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    schedule.every().day.at("12:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    #schedule.every().day.at("15:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    schedule.every().day.at("18:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)
    #    #schedule.every().day.at("21:00").do(main, input_api_nasdaq, output_filename4, subs_membercount_min1, marketcap_max4)

    ##while True:
    # #   schedule.run_pending()
    

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
    # WAY 2 - run program by fixed interval (old)
    *****************************************************************************'''
    #for n in range(20):
    #    ##main(csvfile1)
    #    main(csvfile6, 'savedtickerstest')
    #    time.sleep(3600)

    #input("Press any key to continue . . . (1) ")
    #input("Press any key to continue . . . (2) ")
    #input("Press any key to continue . . . (3) ")
    #input("Press any key to continue . . . (4) ")


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
    
    # run_batch_of_processes_1() ##immediate, test

    # while True:   
    #   schedule.run_pending()


    
    
    
    