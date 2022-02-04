import pathlib, os, time, sys
import ast, requests, pprint


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
# script 8 - playing with pymysql
*****************************************************************************'''


import pymysql

# Connect to the database
connection = pymysql.connect(
                        host=os.environ.get('MYSQL_HOST'),
                        user=os.environ.get('MYSQL_USER'),
                        password=os.environ.get('MYSQL_PASSWORD'),
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
# print(connection)



# try:
#     cursor = connection.cursor()
#     cursor.execute("""show databases;""")
#     result = cursor.fetchall()
#     pprint.pprint(result)

#     cursor.execute("""use helloworld;""")

#     cursor.execute("""select * from table1;""")
#     cursor = connection.cursor()
#     result = cursor.fetchall()
#     pprint.pprint(result)
# finally:
#     connection.close()



# with connection:
#     with connection.cursor() as cursor:
#         # #show databases;
#         sql = "SHOW databases;"
#         cursor.execute(sql)
#         # result = cursor.fetchone()
#         result = cursor.fetchall()
#         print(result)

#     with connection.cursor() as cursor:
#         # #use helloworld;
#         sql = "USE helloworld;"
#         cursor.execute(sql)

#     with connection.cursor() as cursor:
#         # #select * from table1;
#         sql = "SELECT * from table1;"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         pprint.pprint(result)

#     with connection.cursor() as cursor:
#         # #select * from table1;
#         sql = "INSERT INTO table1 values(8, 'john', 'C');"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         pprint.pprint(result)

#     # # connection is not autocommit by default. So you must commit to save
#     # # your changes.
#     connection.commit()



# with connection:
    ### show databases
    # print('\n')
    # with connection.cursor() as cursor:
    #     sql = "SHOW databases;" #show databases;
    #     cursor.execute(sql)

    #     # result = cursor.fetchone()
    #     result = cursor.fetchall()

    #     pprint.pprint(result)


    ##get list of rows within a table
    # print('\n')
    # with connection.cursor() as cursor:
    #     sql = "USE helloworld;" #use a database: helloworld; #works with another cursor.execute(sql) but result doesn't print all commands, but only most recent command
    #     cursor.execute(sql)
    #     sql = "SELECT * from table1;" #select * from table1; 
    #     cursor.execute(sql)
    #     sql = "SELECT * from table2;" #select * from table1; #only this latest command shows in result
    #     cursor.execute(sql)
        
    #     result = cursor.fetchall()
        
    #     #pprint.pprint(result) #print a list of rows as dictionary
    #     for (table_name) in result: #print rows as dictionary (seems to have accurate arrangement of columns)
    #         print(table_name)


    # ###get list of dictionary of table data (ex: [{table1 data}, {table2 data}])
    # ###table data includes table name, table comment, data length, table schema, etc.
    # print('\n')
    # with connection.cursor() as cursor:
    #     sql = "SELECT * FROM information_schema.tables WHERE table_schema = 'helloworld'"
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     for a in result:
    #         print(a["TABLE_NAME"]) #table name from {table data}
    #         # print(a) #{table data}


    # ### find if table exists (within table_schema)
    # print('\n')
    # with connection.cursor() as cursor:
    #     table_schema = 'helloworld'
    #     table_name = 'table1'
    #     sql = f"SELECT * FROM information_schema.tables WHERE table_schema = '{table_schema}' AND table_name = '{table_name}'"
    #     cursor.execute(sql)
    #     result = cursor.fetchall()
    #     # pprint.pprint(result)
        
    #     table_schema = 'helloworld'
    #     table_name = 'table99'
    #     # sql = f"SELECT * FROM information_schema.tables WHERE table_name = '{table_name}'"
    #     # sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{table_schema}'"
    #     sql = f"SELECT * FROM information_schema.tables WHERE table_schema = '{table_schema}' AND table_name = '{table_name}'"
        
    #     if cursor.execute(sql) == 0: #0 = doesn't exist 
    #         print('this table doesnt exists')
    #         print(False)
    #     elif cursor.execute(sql) == 1: #1 = exists
    #         print('this table exists')
    #         print(True)
        
    #         result = cursor.fetchall()
            
    #         pprint.pprint(result)
    #         for a in result:
    #             print(a["TABLE_NAME"]) #table name from {table data}
    #             # print(a) #{table data}
    

    # ###


    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()


#create database, table on aws
with connection:
    # ### find if database exists (within table_schema), get last one, and create another table..

    ### check if database exists, if not.. create one, check if certain table exists, if not.. create one, then check if rows exist, if not, create one
    
    # print('\n')
    # with connection.cursor() as cursor:
    #     sql = f"USE helloworld;"
    #     cursor.execute(sql)

    #     # ###create table
    #     # table_name = 'table4'
    #     # sql = f"CREATE TABLE table4 (id INT, computer_name TEXT);"
    #     # cursor.execute(sql)
        
    #     # ###drop table
    #     # table_name = 'table4'
    #     # sql = f"DROP TABLE table4"
    #     # cursor.execute(sql)

    #     result = cursor.fetchall()
    #     pprint.pprint(result)
   
    
    print('\n')
    with connection.cursor() as cursor:
        
        #create new table in target schema/database
        table_name = "table4"
        table_schema = "helloworld"

        
        #check if table exists
        sql = f"USE {table_schema}"
        cursor.execute(sql)
        sql = f"SELECT * FROM information_schema.tables WHERE table_schema = {table_schema} AND table_name = {table_name}"
        
        if cursor.execute(sql) == 1: #1 = exists
            print(f"table {table_name} already exists")

            ###drop table
            print(f"deleting {table_name}")
            sql2 = f"DROP {table_name}"
            cursor.execute(sql2)
        
        elif cursor.execute(sql) == 0: #0 = doesn't exist 
            

            #create table
            print(f"creating {table_name}")
            sql2 = f"CREATE TABLE {table_name} (id INT, computer_name TEXT);"
            cursor.execute(sql2)
            
        
        result = cursor.fetchall()
        pprint.pprint(result)  




#select * from database1.table2

#select * from helloworld.table1 where name LIKE '___a'; #____s; #not sensitive to lowcase/uppercase
#select * from helloworld.table1 where name LIKE '%a'; #a% #%a%  #not sensitive to lowcase/uppercase

#select * from helloworld.table1 where date >= '1000-01-01' and date <= '1000-02-01'; #DATE
#select * from helloworld.table1 where date between '1000-01-01' and '1000-02-01';    #DATE

#select * from helloworld.table1 where name REGEXP 'matt'; #containing
#select * from helloworld.table1 where name REGEXP '^at'; #beginning
#select * from helloworld.table1 where name REGEXP 'att$'; #ending
#select * from helloworld.table1 where name REGEXP 'mat|bo'; #logical or
#select * from helloworld.table1 where name REGEXP 'mat|bo|flo'; #logical or
#select * from helloworld.table1 where name REGEXP '^ma|ot$'; #logical or + beginning + ending
#select * from helloworld.table1 where name REGEXP 'm[abc]'; #containing any one of letters in bracket
#select * from helloworld.table1 where name REGEXP 'm[a-f]'; #containing any one of letter range in bracket 

#SELECT DISTINCT name from helloworld.table1;

#select * from helloworld.table1 ORDER BY name;
#select * from helloworld.table1 ORDER BY name DESC;
#select * from helloworld.table1 ORDER BY name, grade;
#select * from helloworld.table1 ORDER BY 2,3;
#select * from helloworld.table1 ORDER BY grade, name;
##select * from helloworld.table1 ORDER BY grade DESC, name DESC;
#select * from database1.table1 ORDER BY quantity * price;

#select * from helloworld.table1 LIMIT 3;
#select * from helloworld.table1 limit 2,100; #2 = don't show first 2 rows, 100 = limit to 100 rows

#select * from table1 join table3 on table1.product_id = table3.product_id;
#select student_id, table1.name, grade, date, table3.product_id, table3.name, table3.price from table1 join table3 on table1.product_id = table3.product_id;
#select student_id, t1.name, grade, date, t3.product_id, t3.name, t3.price from table1 t1 join table3 t3 on t1.product_id = t3.product_id;#