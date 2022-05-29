import pathlib, os, time, sys
import ast, requests, pprint
import pandas as pd
import datetime

'''*****************************************************************************
# script 0 - create a set ({}) of all possible tickers (including stocks/crypto) from polygon.io, then save to file
*****************************************************************************'''
# path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + '/..'))
# tickerlist = {'a'}

# apikeyforurl1 = "&apiKey=xxxxx"
# url = "https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&sort=ticker&order=asc&limit=1000&apiKey=xxxxx" #stocks
# #url = "https://api.polygon.io/v3/reference/tickers?market=crypto&active=true&sort=ticker&order=asc&limit=1000&apiKey=xxxxx" #crypto
# r = requests.get(url)
# j = r.json()
# # for k,v in j.items():
# #     print(k)

# # print(type(j["results"]))
# # for a in j["results"][:10]:
# #     print(a["ticker"], a["name"])
# #     tickerlist1.add(a["ticker"])

# # #stocks
# while True:
#     try:
#         print(j["count"])
#         print(j["next_url"], j["request_id"])
#         print(j["results"])
#         for a in j["results"]: #j["results"] = list
#             tickerlist.add(a["ticker"])

#         url = j["next_url"]+apikeyforurl1
#         r = requests.get(url)
#         j = r.json()

#         time.sleep(20)
#     except KeyError:
#         break

# #cryptos (no while loop cuz polygon has less than 1000 cryptos)
# # print(j["count"])
# # for a in j["results"]: #j["results"] = list
# #     tickerlist.add(a["base_currency_symbol"])

# #create and write to text file
# targetfile1 = str(pathlib.Path(path_repo + '/test_output1/tickerlist2.txt'))
# f=open(targetfile1,'w',encoding='UTF-8') 
# f.write(str(tickerlist)) 
# f.close()


'''*****************************************************************************
# script 1 - read text file that contains dictionary (python)
*****************************************************************************'''
# # # path of repo (wip)
# path_repo = str(pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + '/..'))

# #create and write to text file
# targetfile1 = str(pathlib.Path(path_repo + '/test_output1/tickerlist2.txt'))
# with open(targetfile1,'r') as f:
#     tickerlist = f.readlines()[0]
#     tickerlist = ast.literal_eval(tickerlist)

# print(len(tickerlist))

# # f.write(str(set(sorted(tickerlist1)))) 
# # f.close()


'''*****************************************************************************
# script 2
*****************************************************************************'''
# set1 = {'a','z','b','c'}
# set2 = {'kk'}
# set3 = set1 | set2 #combine 2 sets
# # print(sorted(dict))
# # print(set(sorted(dict)))
# print(set3)


'''*****************************************************************************
# script 3
*****************************************************************************'''
# is64bit = sys.maxsize > 2**32
# print('is64bit:',is64bit)


# Filename: using_name.py

# if __name__ == '__main__':
#     print('This program is being run by itself')
# else:
#     print('I am being imported from another module')



'''*****************************************************************************
# script 4
*****************************************************************************'''
# apikeyforurl1 = "&apiKey=xxxxx"
# url = "https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&sort=ticker&order=asc&limit=1000&apiKey=xxxxx" #stocks
# #url = "https://api.polygon.io/v3/reference/tickers?market=crypto&active=true&sort=ticker&order=asc&limit=1000&apiKey=xxxxx" #crypto
# r = requests.get(url)
# j = r.json()
# # for k,v in j.items():
# #     print(k)

# IEX_TOKEN = os.environ.get('IEX_TOKEN')
# IEX_TOKEN = F'?token={IEX_TOKEN}' 
# url = 'https://cloud.iexapis.com/stable/stock/twtr/quote' + '/filter=marketcap' + IEX_TOKEN
# # GET /stock/market/list/{list-type}
# url = 'https://cloud.iexapis.com/stable/stock/markeatch' + '?symbt/batch' + '?symbols=aapl,fb,tsla&types=quote,news,chart&range=1m&last=5' + IEX_TOKEN
# url = 'https://cloud.iexapis.com/stable/stock/market/bols=aapl,fb,tsla' + IEX_TOKEN
# url = 'https://cloud.iexapis.com/stock/aapl/batch?types=quote,news,chart&range=1m&last=10' + IEX_TOKEN
# url = 'https://cloud.iexapis.com/stable/stock/twtr/quote/marketCap' + IEX_TOKEN



# for k,v in ast.literal_eval(j.items()):
#     print(k,v)

# for a in j:
#     print(a['symbol'], a['marketCap'])

'''*****************************************************************************
# script 5 - get multiple values from one stock symbol/url
*****************************************************************************'''
# IEX_TOKEN = os.environ.get('IEX_TOKEN')
# IEX_TOKEN_url = F'?token={IEX_TOKEN}'  
# IEX_TOKEN_url_batch = F'&token={IEX_TOKEN}'

# url = 'https://cloud.iexapis.com/stable/stock/' + 'aapl' + '/quote' + IEX_TOKEN_url
# #url = 'https://cloud.iexapis.com/stable/stock/' + 'aapl' + '/batch?types=quote' + IEX_TOKEN_url_batch

# r = requests.get(url)
# print(r)
# j = r.json()
# # pprint.pprint(j)
# # print(j["quote"]["marketCap"])
# # print(j["quote"]["latestPrice"])

# print(j["marketCap"], j["latestPrice"])


'''*****************************************************************************
# script 6 - print cut off strings
*****************************************************************************'''
# print('saldkfjasdklgj'[:10])



'''*****************************************************************************
# script 7 - try out sandbox IEX
*****************************************************************************'''
# IEX_TOKEN_SANDBOX = os.environ.get('IEX_TOKEN_SANDBOX')
# IEX_TOKEN_SANDBOX = F'?token={IEX_TOKEN_SANDBOX}' 

# k = 'aapl'
# #url = 'https://cloud.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN
# url =  'https://sandbox.iexapis.com/stable/stock/' + str(k) + '/quote' + IEX_TOKEN_SANDBOX

# r = requests.get(url)
# print(r)
# j = r.json()
# print(j)

'''*****************************************************************************
# script 8 - use datetime module (to insert into sql table, instead of using now())
*****************************************************************************'''

print(datetime.datetime.now())
time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(time1, type(time1))

#'2011-12-18 13:17:17'
#'05/19/2022 23:02:00'
