'''includes US stock symbols with market cap > 100 Million, and price above $3. 
Download the csv file  https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download 
of all the NYSE, NASDAQ and NYSEAMERICAN public traded companies.
'''

import requests, csv, sys, pathlib, os, ast, shutil, pandas as pd
from numpy import int_
from requests_toolbelt import user_agent
# from urllib.request import urlretrieve
import urllib.request


'''*****************************************************************************
# variables of file paths
*****************************************************************************'''
path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + '/..'))
path_listsubscsv = '/rsa/listsubs.csv'
path_repo_and_listsubscsv = str(pathlib.Path(path_repo + path_listsubscsv))

# step 1
def getlist_subreddits(parameter_subs):

    subs_local = []
    
    df = pd.read_csv(path_repo_and_listsubscsv) # READS FINE, ERROR IF APPENDING TO LIST (see codes ahead)

    ####way 1 - get a list of subs
    #for row in df['Subreddit']:
    #    subs.append(row)
    
    
    # ####way 2 - get a list of subs but only the ones with over x members # CAUSES MEMORY ERROR ON AWS LINUX..? Fix it....
    # if isinstance(parameter_subs,int):
    #     list_subs = []
    #     for row in df['Subreddit']:
    #         list_subs.append(row)
    #         #print(list_subs)
    #     list_members = []
    #     for row in df['Members']:
    #         list_members.append(row)
    #         #print(list_members)

    #     for a in list_subs:
    #         index = list_subs.index(a)
    #         if list_members[index] >= parameter_subs:
    #             subs_local.append(a)
    #     #print(subs_local)
    #     #print(len(subs_local))


    # possible solution - working..
    # ####way 3 - 
    #print("df['Subreddit']:", type(df['Subreddit']), df['Subreddit'])
    #print("df['Members']:", type(df['Members']), df['Members'])
    #print("df['Subreddit']:", type(df['Subreddit']), df['Subreddit'])
    if isinstance(parameter_subs,int):
        #WORKing
        list_subs = []
        for row in df['Subreddit']:
            list_subs.append(row)
            #print(list_subs)
        list_members = []
        for row in df['Members']:
            list_members.append(row)
            #print(list_members)
        #print('list_subs:', len(list_subs), list_subs) #log
        #print('list_members:', len(list_members), list_members) #log

        df = None #try it with below codes
        #WORKing
        for a in list_subs:
            index = list_subs.index(a)
            if list_members[index] >= parameter_subs:
                subs_local.append(a)
        #print('subs_local:', len(subs_local), subs_local) #log

    elif isinstance(parameter_subs,list): 
        subs_local = parameter_subs
    #
    #
    # possible solution

    ##explore panda 
    ##explore panda 
    #print(type(df['Members']), 'atype def members')
    ##print(df.to_dict())

    #for k,v in df.to_dict().items():
    #    print('oop', k,v)

    #for k,v in df.items():
    #    print(k,v, 'rowdf')

    # print(str(df))
    ##explore panda
    ##explore panda 

    # print(subs_local)
    return subs_local


# step 2
def getlist_nasdaq_csvfile(csvfile):
    us_local = {'a'}

    with open(csvfile,'r') as f:
        lines = f.readlines()

    headers=lines[0].rstrip().split(',') # rstrip removes end-of-line chars
    numLines = len(lines)
    linelist = [x.rstrip().split(',') for x in lines[1:numLines+1]]    
    # create lineList to include only numLines elements
    outputDict = {keyVal:[x[idx] for x in linelist if len(x)==len(headers)] for idx,keyVal in enumerate(headers)}   

    # list comprehension within dictionary comprehension to split each element by its header and create dictionary of lists 
    # print(outputDict)

    #us = {'a'} #global only
    
    for u in outputDict['Symbol']:
        us_local.add(u)

    listy = ['ADA', 'SOL', 'LTC', 'ETH', 'BNB', 'KNI', 'BTC', 'ADA', 'DOGE', 'BCH', 'XLM', 'NANO', 'INTP','TTCF','GOEV']
    for u in listy:
        us_local.add(u)
       
    #x = list(us_local)
    #print(x[10], x[20])
    #print(len(us_local), ' -- len(us)2_1')
    
    print("getlist_nasdaq_csvfile function end")
    return us_local

def download_file1(url):
    print('download_file1 started')

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }

    # local_filename = url.split('/')[-1]
    # with requests.get(url, headers=headers, stream=True) as r:
    #     with open(local_filename, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    # return local_filename

    ##example0
    # path_newtextfile = path_repo + '/textfile3.txt'    
    # with requests.get(url, headers=headers, stream=True) as r:
    #     with open(path_newtextfile, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    # return path_newtextfile

    ##example1
    path_newtextfile = path_repo + '/textfile3.txt'    
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(path_newtextfile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk: 
                f.write(chunk)
                print(chunk)
    return path_newtextfile
def download_file_separate(url):
    print('download_file_separate(url) started ID 2')
     # local_filename = url.split('/')[-1]
    path_newtextfile = path_repo + '/textfile_separate.txt'

    
    #random header i guess
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    # }
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebK it/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    # }
    # headers = {
    #     'User-Agent': 'My User Agent 1.0' 
    # }
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # }
    # headers = {'user-agent':'text'}

    

    #test test

    #response = requests.get(url, stream=True)
    #response = requests.get('https://api.github.com') # works, used response.json() to test
    #response = requests.get(url) # api nasdaq website itself causes error/stuck?
    #response = requests.get(url, headers=headers, stream=True) # api nasdaq website itself causes error/stuck?
    #response = requests.get(url, headers=headers, timeout=5) #
    #response = requests.get('https://api.github.com', headers=headers, timeout=5, stream=True) #0 with 'txt' headers and api github, 1
    # with requests.get(url, headers=headers, stream=True, timeout=10) as r:
    #     with open(path_newtextfile, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)

    #print(response.json())

    #print('requests get executed')
    #test test

    # way 1
    # with requests.get(url, headers=headers, stream=True) as r:
    # #with requests.get(url, stream=True) as r:
    #     with open(path_newtextfile, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    
    # way 2
    #r = requests.get(url, stream=True) #try without headers on aws
    # r = requests.get(url, headers=headers, stream=True) #use headers on local windows machine, or try on linux with different header
    # if r.ok:
    #     with open(path_newtextfile, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=1024 * 8):
    #             if chunk:
    #                 f.write(chunk)
    #                 f.flush()
    #                 os.fsync(f.fileno())
    # else:  # HTTP status code 4XX/5XX
    #     print("Download failed: status code {}\n{}".format(r.status_code, r.text))

    # way 3
    #r = requests.get(url) #
    
    # way 4
    # r = urllib.request.urlopen(url)
    # print(r.read())
    

    # way 5


    print('download_file_separate(url) ended')
    # # return path_newtextfile
    
def getlist_nasdaq_api(marketcap_min, marketcap_max):
    # temporary variable, should be global
    #marketcap_min = 50000000000

    us_local = {'a'}
    mc_local = {}
    price_local = {}
    pctchange_local = {}
    name_local = {}
    

    #### obtain data from api.nasdaq.com
    #### 
    #### 
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }

    #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nyse"
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=20000"
    # url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=5" #try smaller

    # r = requests.get(url, headers=headers, stream=True) #causes MEMORY ERROR
    # j = r.json()
    # print(sys.getsizeof(j))

    #a DICT? - log print
    #print(j)
    #for a in j:
    #    print(a)
    #data
    #message
    #status

    #a DICT - log print
    #print(j['data'])
    #for k,v in j['data'].items():
    #    print(k,v)
    #filters
    #table
    #totalrecords

    #a DICT - log print
    #for k,v in j['data'].get('table').items():
    #    print(k,v)
    #heads
    #rows

    # #a DICT - log print
    #print(type(j['data'].get('table').get('rows')))
    #num1 = 0;
    #for v in j['data'].get('table').get('rows'):
    #    if num1 < 5:
    #        print(v)
    #        num1 += 1
    #    else:
    #        break
    #print(v) #row in dictionary form
    #print(v.get('symbol'), v.get('marketCap'), marketCap) #showing only symbol and marketCap

    
    # WAY 1
    #a LIST of row in dictionary form (containing stock, marketCap, etc)
    for v in j['data'].get('table').get('rows'):
    #for v in j['data'].get('table').get('rows')[:5]: #shortened to test aws small memory computer
        try:
            marketCap = int(v.get('marketCap').replace(',', ''))
            lastsale = float(v.get('lastsale').replace('$', '').replace(',', ''))
            pctchange = float(v.get('pctchange').replace('%', ''))
            name = (" " + str(v.get('name'))).replace('"', '')

            #if marketCap <= 200000000000:
            if marketCap <= marketcap_max and marketCap >= marketcap_min:
                us_local.add(v.get('symbol')) 
                mc_local[v.get('symbol')] = "$%.2f" % (marketCap/1000000000) + "B" #{symbol: marketcap}
                price_local[v.get('symbol')] = "${:.2f}".format(lastsale) #{symbol: lastsale}
                pctchange_local[v.get('symbol')] = "{:.2f}%".format(pctchange) #{symbol: pctchange}
                name_local[v.get('symbol')] = name

                #print("{:.2f}%".format(lastsale),"{:.2f}%".format(pctchange)) #log
            else:
                continue
        except:
            #skip NA
            continue

    #print(len(j['data'].get('table').get('rows')), type(j['data'].get('table').get('rows')))

    #### 
    #### 
    #### obtain data from api.nasdaq.com

    return us_local, mc_local, price_local, pctchange_local, name_local
def getlist_from_textfile():
     # #TEMPORARY SOLUTION:
    #print('getlist_from_textfile() started')
    
    # way 1, 2
    # us_local = {'AAPL', 'GOOG', 'GOOGL', 'a', 'AMZN', 'MSFT'}
    # us_local = {'STLA', 'ZM', 'ETN', 'NFLX', 'UNH', 'SAP', 'LRCX', 'NVDA', 'SO', 'RACE', 'RIO', 'HDB', 'TEAM', 'BSX', 'NVO', 'SONY', 'CHTR', 'LMT', 'FTNT', 'UNP', 'SNPS', 'IBM', 'CDNS', 'MRVL', 'NIO', 'PBR', 'PTR', 'COIN', 'USB', 'JCI', 'a', 'SNY', 'TFC', 'DG', 'AMD', 'PG', 'AMAT', 'BX', 'IBN', 'HSBC', 'BUD', 'MUFG', 'MCD', 'VZ', 'HD', 'BIDU', 'DUK', 'CMCSA', 'NVS', 'ADP', 'LULU', 'ADI', 'UL', 'ECL', 'MET', 'LIN', 'PSA', 'CVX', 'MCO', 'SQ', 'ITW', 'MDLZ', 'EXC', 'MELI', 'BBL', 'BHP', 'MSCI', 'TSM', 'BKNG', 'XLNX', 'KDP', 'LLY', 'MS', 'WM', 'SHW', 'APD', 'HCA', 'ANTM', 'CL', 'FB', 'WFC', 'QCOM', 'TM', 'CSCO', 'NGG', 'TEL', 'C', 'EL', 'FCX', 'TTE', 'MO', 'UBER', 'ICE', 'BDX', 'FDX', 'WBK', 'ISRG', 'UBS', 'RTX', 'F', 'EW', 'AMOV', 'ABT', 'COP', 'GOOG', 'V', 'SE', 'PFE', 'MU', 'D', 'MSFT', 'PNC', 'NKE', 'CRM', 'ING', 'BABA', 'DXCM', 'DHR', 'BNTX', 'ABB', 'NTES', 'SYK', 'IDXX', 'COST', 'FIS', 'GD', 'TJX', 'EOG', 'CCI', 'CI', 'BMO', 'TRI', 'BLK', 'CME', 'JPM', 'RIVN', 'AAPL', 'ABNB', 'BTI', 'PDD', 'BAM', 'PANW', 'GM', 'SNAP', 'TMUS', 'CB', 'COF', 'HUM', 'ABBV', 'INTC', 'INFO', 'AMZN', 'LOW', 'ENB', 'SCHW', 'PM', 'NOW', 'GE', 'BNS', 'INFY', 'ORCL', 'RELX', 'MA', 'RY', 'SPGI', 'TGT', 'XOM', 'AXP', 'NEE', 'ILMN', 'SNP', 'DASH', 'IQV', 'KO', 'MRK', 'DE', 'PEP', 'AMGN', 'PLD', 'AMT', 'TD', 'PGR', 'VALE', 'GOOGL', 'SAN', 'TSLA', 'WMT', 'GS', 'XPEV', 'ADSK', 'ACN', 'VRTX', 'CAT', 'ZTS', 'NOC', 'GSK', 'NSC', 'UPS', 'DEO', 'AZN', 'MRNA', 'EQNR', 'KLAC', 'BMY', 'EQIX', 'FISV', 'DDOG', 'BAC', 'DIS', 'MDT', 'JNJ', 'NXPI', 'CNI', 'SHOP', 'AVGO', 'TMO', 'SNOW', 'AMX', 'ASML', 'GILD', 'BP', 'AON', 'ADBE', 'TXN', 'HON', 'MAR', 'INTU', 'T', 'LCID', 'PYPL', 'SBUX', 'JD', 'MMC', 'CSX', 'EMR', 'ROP', 'MMM', 'WDAY', 'BA', 'RBLX', 'CVS', 'REGN'}
    
    # way 3 - read from text file
    targetfile = str(pathlib.Path(path_repo + '/test_output1/tickerlist1.txt'))
    f = open(targetfile,'r')
    us_local = f.readlines()[0]
    us_local = ast.literal_eval(us_local)
    f.close()
    targetfile = str(pathlib.Path(path_repo + '/test_output1/tickerlist3.txt')) #crypto symbols list from IEX #should convert from polygon to IEX.. symbol by symbol
    f = open(targetfile,'r')
    us_local2 = f.readlines()[0]
    us_local2 = ast.literal_eval(us_local2)
    f.close()
    us_local = us_local | us_local2 #combine 2 sets
    
    return us_local
    
    # mc_local = {'AAPL': '$3035.xB', 'MSFT': '$2514.xB', 'GOOG': '$1974.xB', 'GOOGL': '$1967.xB', 'AMZN': '$1786.xB'}
    # price_local = {'AAPL': '$175.x', 'MSFT': '$334.x', 'GOOG': '$2974.x', 'GOOGL': '$2963.x', 'AMZN': '$3523.x'}
    # pctchange_local = {'AAPL': '2.x%', 'MSFT': '0.x%', 'GOOG': '0.x%', 'GOOGL': '0.x%', 'AMZN': '-0.x%'}
    # name_local = {'AAPL': ' Apple Inc. Common Stock', 'MSFT': ' Microsoft Corporation Common Stock', 'GOOG': ' Alphabet Inc. Class C Capital Stock', 'GOOGL': ' Alphabet Inc. Class A Common Stock', 'AMZN': ' Amazon.com, Inc. Common Stock'}
    # return us_local, mc_local, price_local, pctchange_local, name_local
 
# separate creating file from api nasdaq from creating variable
def getlist_nasdaq_api_chunk(marketcap_min, marketcap_max):
    # temporary variable, should be global
    #marketcap_min = 50000000000

    us_local = {'a'}
    mc_local = {}
    price_local = {}
    pctchange_local = {}
    name_local = {}

    #### obtain data from api.nasdaq.com
    #### 
    #### 
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    # headers = {
    # 'User-Agent': user_agent('my_package', '0.0.1')
    # }

   
    #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=3296&exchange=nyse"
    #url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=20000"
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=1" #try smaller

    
    # r = download_file1(url)
    # f = open(r) 
    # print (f.read())
    

    #r = requests.get(url, headers=headers, stream=True) #causes MEMORY ERROR
    #r = requests.get(url, headers=headers) 
    #j = r.json()

    
    #print(type(r))
    #print('r:', r.json())
    #print('r:', type(r))
    # print(sys.getsizeof(j))


    # url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=1"
    # dst = 'stocks?tableonly=true&limit=1'
    # urlretrieve(url, dst)


    '''*****************************************************************************
    # 
    *****************************************************************************'''

    #a DICT? - log print
    #print(j)
    #for a in j:
    #    print(a)
    #data
    #message
    #status

    #a DICT - log print
    #print(j['data'])
    #for k,v in j['data'].items():
    #    print(k,v)
    #filters
    #table
    #totalrecords

    #a DICT - log print
    #for k,v in j['data'].get('table').items():
    #    print(k,v)
    #heads
    #rows

    # #a DICT - log print
    #print(type(j['data'].get('table').get('rows')))
    #num1 = 0;
    #for v in j['data'].get('table').get('rows'):
    #    if num1 < 5:
    #        print(v)
    #        num1 += 1
    #    else:
    #        break
    #print(v) #row in dictionary form
    #print(v.get('symbol'), v.get('marketCap'), marketCap) #showing only symbol and marketCap


    
    # WAY 1
    #a LIST of row in dictionary form (containing stock, marketCap, etc)
    # for v in j['data'].get('table').get('rows'):
    # #for v in j['data'].get('table').get('rows')[:5]: #shortened to test aws small memory computer
    #     try:
    #         marketCap = int(v.get('marketCap').replace(',', ''))
    #         lastsale = float(v.get('lastsale').replace('$', '').replace(',', ''))
    #         pctchange = float(v.get('pctchange').replace('%', ''))
    #         name = (" " + str(v.get('name'))).replace('"', '')

    #         #if marketCap <= 200000000000:
    #         if marketCap <= marketcap_max and marketCap >= marketcap_min:
    #             us_local.add(v.get('symbol')) 
    #             mc_local[v.get('symbol')] = "$%.2f" % (marketCap/1000000000) + "B" #{symbol: marketcap}
    #             price_local[v.get('symbol')] = "${:.2f}".format(lastsale) #{symbol: lastsale}
    #             pctchange_local[v.get('symbol')] = "{:.2f}%".format(pctchange) #{symbol: pctchange}
    #             name_local[v.get('symbol')] = name

    #             #print("{:.2f}%".format(lastsale),"{:.2f}%".format(pctchange)) #log
    #         else:
    #             continue
    #     except:
    #         #skip NA
    #         continue

    #print(len(j['data'].get('table').get('rows')), type(j['data'].get('table').get('rows')))

    print("empty us_local, etc. variables received and..")
    return us_local, mc_local, price_local, pctchange_local, name_local






## includes common words and words used on wsb that are also stock names
blacklist = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR','DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar'}

# adding wsb/reddit flavour to vader to improve sentiment analysis, score: 4.0 to -4.0
new_words = {
    'citron': -4.0,  
    'hidenburg': -4.0,        
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,    
    'put': -4.0,
    'puts': -4.0,    
    'break': 2.0,
    'tendie': 2.0,
        'tendies': 2.0,
        'town': 2.0,     
        'overvalued': -3.0,
        'undervalued': 3.0,
        'buy': 4.0,
        'sell': -4.0,
        'gone': -1.0,
        'gtfo': -1.7,
        'paper': -1.7,
        'bullish': 3.7,
        'bearish': -3.7,
        'bagholder': -1.7,
        'stonk': 1.9,
        'green': 1.9,
        'money': 1.2,
        'print': 2.2,
        'rocket': 2.2,
        'bull': 4.0,
        'bear': -4.0,
        'pumping': -1.0,
        'sus': -3.0,
        'offering': -2.3,
        'rip': -4.0,
        'downgrade': -3.0,
        'upgrade': 3.0,     
        'maintain': 1.0,          
        'pump': 1.9,
        'hot': 1.5,
        'drop': -2.5,
        'rebound': 1.5,  
        'crack': 2.5,
    'gang': 2.0,
        'scam': -2.0,
    'chamath': -2.0,
        'snake': -2.0,
    'squezze': 3.0,
        'bag': -4.0,
        'fly': 2.0,     
        'way': 2.0,     
        'high': 2.0,
        'volume': 2.5,
        'low': -2.0,
        'trending': 3.0,
        'upwards': 3.0,
        'prediction': 1.0,     
        'cult': -1.0,     
    'big': 2.0,}