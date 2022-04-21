from asyncore import close_all
import pathlib, os, time, sys
import ast, requests, pprint
from matplotlib.pyplot import table
from pymysql import NULL
import pandas as pd


'''*****************************************************************************
# script 8 - playing with pymysql
*****************************************************************************'''

table_name1 = "result_test_"
database_name1 = "rsa_db"

import pymysql

# Connect to the database
connection = pymysql.connect(
                        host=os.environ.get('MYSQL_HOST_RDS'),
                        user=os.environ.get('MYSQL_USER_RDS'),
                        password=os.environ.get('MYSQL_PASSWORD_RDS'),
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
# print(connection)

# cursor = connection.cursor()

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

# with connection:

#     ### find if table exists (within table_schema)
#     print('\n')
#     with connection.cursor() as cursor:
#         # database_name1 = 'rsa_db'
#         # table_name1 = 'table1'
#         # sql = f"SELECT * FROM information_schema.tables WHERE table_schema = '{database_name1}' AND table_name = '{table_name1}'"
#         # cursor.execute(sql)
#         # result = cursor.fetchall()
#         # pprint.pprint(result)

#         database_name1 = 'rsa_db'
#         table_name1 = 'table1'
#         # sql = f"SELECT * FROM information_schema.tables WHERE table_name = '{table_name}'"
#         sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database_name1}' AND TABLE_NAME = '{table_name1}'"
#         #sql = f"SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{database_name1}') AND (TABLE_NAME = '{table_name1}')"
        
        
#         if cursor.execute(sql) == 0: #0 = doesn't exist 
#             print('this table doesnt exists')
#             print(False)

#             result = cursor.fetchall()
#             pprint.pprint(result)

#         elif cursor.execute(sql) == 1: #1 = exists
#             print('this table exists')
#             print(True)
        
#             result = cursor.fetchall()
#             pprint.pprint(result)
    

#     ###


#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()






# create database, table on aws
#with connection:
    ### find if database exists (within table_schema), get last one, and create another table..

    ## check if database exists, if not.. create one, check if certain table exists, if not.. create one, then check if rows exist, if not, create one
    
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
   
    # print('\n')
    # with connection.cursor() as cursor:
        
    #     #create new table in target schema/database
    #     table_name1 = "table1"
    #     database_name1 = "rsa_db"

        
    #     # # check if table exists
    #     # sql = f"USE {database_name1}"
    #     # cursor.execute(sql)
    #     sql = f"SELECT * FROM information_schema.tables WHERE table_schema = '{database_name1}' AND table_name = '{table_name1}'"
        
    #     if cursor.execute(sql) == 1: #1 = exists
    #         print(f"TABLE {table_name1} already exists")
    #         ###drop table
    #         # print(f"deleting {table_name}")
    #         # sql2 = f"DROP {table_name}"
    #         # cursor.execute(sql2)
        
    #     elif cursor.execute(sql) == 0: #0 = doesn't exist 
    #         print(f"TABLE {table_name1} doesn't exists")
    
    #         #create table
    #         # print(f"creating {table_name}")
    #         # sql2 = f"CREATE TABLE {table_name} (id INT, computer_name TEXT);"
    #         # cursor.execute(sql2)
                   
    #     result = cursor.fetchall()
    #     pprint.pprint(result)  


#         #check if table exists 2 
#         stmt = f"SHOW TABLES LIKE '{table_name1}'"
#         cursor.execute(stmt)
# result = cursor.fetchone()
    


# #print list of tables 1
# with connection:
#     with connection.cursor() as cursor:

#         #way 1 - show tables
#         # cursor.execute("USE helloworld;")
#         # cursor.execute("Show tables;")

#         #way 2 - show tables
#         cursor.execute("SHOW tables FROM helloworld;")
 
#         #for way 1-3 below
#         myresult = cursor.fetchall()

#         # #way 1 - print k,v from list of tables dict
#         # for c in myresult:
#         #     print(c, c.keys(), c.values())
#         #     #print(c, list(c.keys())[0], list(c.values())[0])

#         # #way 2 - print k,v from list of tables dict
#         # for c in cursor:
#         #     print(c, c.keys(), c.values())
#         #     #print(c, list(c.keys())[0], list(c.values())[0])
        
#         #way 3 - print k,v from list of tables dict
#         for c in myresult:
#             for k,v in c.items():
#                 #print(k, v)
#                 print(v)


#         #count tables if table contains " "
#         # print(len(myresult))

# #print list of tables 2
# with connection:
#     with connection.cursor() as cursor:
#         database_name1 = 'helloworld'

#         cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}';")

#         myresult = cursor.fetchall()

#         for c in myresult:
#             for k,v in c.items():
#                 #print(k, v)
#                 print(v)


##get a list of existing saved tables that contains given outputfilename_custom
# with connection:
#     with connection.cursor() as cursor:
#         database_name1 = 'helloworld'
#         table_name1 = 'table'

#         cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND table_name like '%{table_name1}%';")

#         myresult = cursor.fetchall()
#         print(myresult)
#         myresult_list = [list(a.values())[0] for a in myresult]
#         print(myresult_list)

#         for c in myresult:
#             for k,v in c.items():
#                 #print(k, v)
#                 print(v)



# #count tables in a database (with specific/similar table name)
# with connection:
#     with connection.cursor() as cursor:

#         #count tables in a database
#         database_name1 = 'helloworld'

#         cursor.execute(f"SELECT COUNT(table_name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}';")

#         myresult = cursor.fetchall()


#         print(myresult)
        
#         count = list(myresult[0].values())[0]
#         print(count)


#         #count tables in a database.. with specific/similar table name
#         #get table count, new number
#         database_name1 = 'helloworld'
#         table_customname1 = 'result'

#         cursor.execute(f"SELECT COUNT(table_name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND table_name like '{table_customname1}%';")

#         myresult = cursor.fetchall()
        
#         print(myresult)
        
#         count_tables = list(myresult[0].values())[0]
#         print(count_tables)

#         newnum1 = count_tables + 1
#         print(newnum1)




# def function_sql1():
#     cursor.execute("show databases;")
#     result = cursor.fetchall()
#     pprint.pprint(result)

# def function_sql2():
#     cursor.execute("select * from helloworld.table1;")
#     result = cursor.fetchall()
#     pprint.pprint(result)


# function_sql1()
# function_sql2()



# # # check if database exists, create one if doesnt exist
# database_name1 = 'sampledb'
# cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name1}';")

# result = cursor.fetchall()
# pprint.pprint(result)

# if result == () or result == None: 
#     print(result, '= None')
#     cursor.execute(f"CREATE DATABASE {database_name1}")
# else:
#     print(result, '= not None')

### connection.commit() # no need..

#### delete database
# database_name1 = 'helloworld2'
# cursor.execute(f"DROP DATABASE {database_name1};")







#create multiple tables in for loops
# for a in range(20):
    
#     a += 1
#     try:

#         #create tables
#         if a < 10:
#             cursor.execute(f"CREATE TABLE {database_name1}.{table_name1}00{str(a)}(tutorial_id INT NOT NULL AUTO_INCREMENT,tutorial_title VARCHAR(100) NOT NULL, tutorial_author VARCHAR(40) NOT NULL, submission_date DATE, PRIMARY KEY ( tutorial_id ));")
#         elif a >= 10 and a < 100:
#             cursor.execute(f"CREATE TABLE {database_name1}.{table_name1}0{str(a)}(tutorial_id INT NOT NULL AUTO_INCREMENT,tutorial_title VARCHAR(100) NOT NULL, tutorial_author VARCHAR(40) NOT NULL, submission_date DATE, PRIMARY KEY ( tutorial_id ));")
#         elif a >= 100 and a < 1000:
#             cursor.execute(f"CREATE TABLE {database_name1}.{table_name1}{str(a)}(tutorial_id INT NOT NULL AUTO_INCREMENT,tutorial_title VARCHAR(100) NOT NULL, tutorial_author VARCHAR(40) NOT NULL, submission_date DATE, PRIMARY KEY ( tutorial_id ));")


    
#     except:
#         continue #ignore existing table, and keep creating new tables



# #delete multiple tables in for loops
# for a in range(5):
#     a += 1
#     cursor.execute(f"DROP TABLE {database_name1}.sample{a};")




# #get list of tables with like name, loop thru the list and change the name numbers
# cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND table_name like '%{table_name1}%';")
# myresult = cursor.fetchall()
# list_sqltables = [list(a.values())[0] for a in myresult]
# print('list_sqltables', list_sqltables) #log



# #then drop tables like table_name1/essentially clear tables in database;
# for a in list_sqltables:
#     cursor.execute(f"DROP TABLE {database_name1}.{a};")

#test: drop first table
# cursor.execute(f"DROP TABLE {database_name1}.{list_sqltables[0]};")
# print("dropped:", f"{database_name1}.{list_sqltables[0]}")

# for a in list_sqltables:
#     num_file = list_sqltables.index(a)+1
#     try:
#         cursor.execute(f"RENAME TABLE {database_name1}.{a} TO {database_name1}.{table_name1}{num_file};")
#     except:
#         continue


# coldata_00 = 0
# coldata_01 = 'stringg1'
# coldata_02 = 2
# coldata_07 = 3.33
# coldata_08 = 4.44
# coldata_09 = 5.55
# coldata_10 = 6.6633
# coldata_11 = 'stringg2'
# coldata_11 = "'%s'" % (coldata_11)
# coldata_12 = 'NULL'

# query0="INSERT INTO %s (tickerId, symbol, mentions, marketCap, latestPrice, changePercent, peRatio, companyName, tableId) VALUES (%i, %s, %i, %f, %f, %f, %f, %s, %i)"
# query0="INSERT INTO %s (tickerId, symbol, mentions, marketCap, latestPrice, changePercent, peRatio, companyName, tableId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

# query0=query0 % (f"{database_name1}.{table_name1}", coldata_00, coldata_01, coldata_02, coldata_07, coldata_08, coldata_09, coldata_10, coldata_11, coldata_12)

# print(query0)


# str1 = "'%s'" % "im weird"
# print(str1)

# str2_0 = 'hello'
# str2 = f"'{str2_0}'"
# print(str2)

# if str2 == "'hello'":
#     print(str2, 'again')

# str3 = "None"
# str4 = None
# print(str3, str4) 
# print(type(str3), type(str4)) 
# if str3 == str4:
#     print('true')

#CREATE TABLE testtable2 (Analysis_Id INT, Symbols VARCHAR(200), Mentions INT, marketCap DECIMAL(16,2), latestPrice DECIMAL(16,2), changePerc DECIMAL(16,2), peRatio DECIMAL(16,2), companyNam Symbols VARCHAR(200), Table_Id INT, PRIMARY KEY (Analysis_Id));





'''*****************************************************************************
#delete excess mysql rows, rename leftover rows = ok 
#get list of parenttable_id =ok
#deleting excessive rows from a child table, =ok
#deleting excessive rows from a parent table =ok
#renaming leftover rows (ex: 5-8 to 1-4, 6-10 to 1-5) =ok
*****************************************************************************'''
max_output_amount = 5
database_name1 = 'test_db1'
table_name1_child = 'result_all_child'
table_name1_parent = 'result_all_parent'
outputname_userinput = 'result_all_'

# #child table
# with connection.cursor() as cursor:
#     print("\nchild table (deleting/renaming):")
#     sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     # pprint.pprint(result)
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)

#     while True:
#         if len(list_existingoutputfiles1) >= max_output_amount:           
#             #delete first rows - sql
#             cursor.execute(f"DELETE FROM {database_name1}.{table_name1_child} where parenttable_id = {list_existingoutputfiles1[0]};")

#             #reinitialize list of tables - sql
#             list_existingoutputfiles1 = []
#             sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#             cursor.execute(sql)

#             result = cursor.fetchall()
#             #turn into list
#             list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#             # remove duplicates
#             list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#             print(list_existingoutputfiles1)
                
#         else:
#             break

#     print('renaming leftover rows')
#     for a in list_existingoutputfiles1:
#         new_parenttable_id = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
#         #old_parenttable_id = a
#         sql = f"UPDATE {database_name1}.{table_name1_child} SET parenttable_id = {new_parenttable_id} where parenttable_id = {a};"
#         cursor.execute(sql)
    
#     #reinitialize list of tables - sql
#     list_existingoutputfiles1 = []
#     sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)
    

# #parent table
# #parent table
# with connection.cursor() as cursor:
#     print("\nparent table (deleting/renaming):")
#     sql = f"select parenttable_id from {database_name1}.{table_name1_parent} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     # pprint.pprint(result)
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)
    
#     while True:
#         if len(list_existingoutputfiles1) >= max_output_amount:           
#             #delete first rows - sql
#             cursor.execute(f"DELETE FROM {database_name1}.{table_name1_parent} where parenttable_id = {list_existingoutputfiles1[0]};")

#             #reinitialize list of tables - sql
#             list_existingoutputfiles1 = []
#             sql = f"select parenttable_id from {database_name1}.{table_name1_parent} order by parenttable_id ASC;"
#             cursor.execute(sql)

#             result = cursor.fetchall()
#             #turn into list
#             list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#             # remove duplicates
#             list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#             print(list_existingoutputfiles1)
                
#         else:
#             break

#     print('renaming leftover rows')
#     for a in list_existingoutputfiles1:
#         new_parenttable_id = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
#         #old_parenttable_id  = a
#         sql = f"UPDATE {database_name1}.{table_name1_parent} SET parenttable_id = {new_parenttable_id} where parenttable_id = {a};"
#         cursor.execute(sql)

#     #reinitialize list of tables - sql
#     list_existingoutputfiles1 = []
#     sql = f"select parenttable_id from {database_name1}.{table_name1_parent} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)

# connection.commit()




# INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (16, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);

'''*****************************************************************************
# add new mysql table
*****************************************************************************'''
def prepare_variables1_sql_onetableversion(outputname_userinput, max_output_amount):
    '''*****************************************************************************
    ### 0 - check if database, parent table, child table exist or doesn't exist yet
    ### 1 - get new ref number (set as 1 if tables dont exist OR get latest/highest parenttable_id from child table if exist)
    ### 2 - adjust the new ref number (parenttable_id + 1) -- (using max_output = 10: 10 if parenttable_id = 10 there already, 10 if 9 there already, 9 if 8 files there already, 1 if 0, 2 if 1)
    # parameters: outputname_userinput, max_output_amount
    # return variables: new_ref_number
    *****************************************************************************'''

    exists_database = None
    exists_parenttable = None
    exists_childtable = None

    print('\nprepare_variables1_sql_onetableversion()*************************')
    print('outputname_userinput:', outputname_userinput)

    ### 0
    #check if database exists
    cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name1}';")
    result = cursor.fetchall()
    if result == () or result == None: 
        print(f"No such database exists.")
        print(f"Will create [{database_name1}] database after sentiment analysis")
        exists_database = False
    else:
        print(result)
        print(f"database exists.. {database_name1} database")
        exists_database = True

    #check if parent table exists
    cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND TABLE_NAME = '{outputname_userinput}parent';")
    result = cursor.fetchall()
    if result == () or result == None: 
        print(f"No such parent table exists.")
        print(f"Will create [{database_name1}.{outputname_userinput}parent] table after sentiment analysis")
        exists_parenttable = False
    else:
        print(result)
        print(f"parent table exists.. [{database_name1}.{outputname_userinput}parent] table")
        exists_parenttable = True

    #check if child table exists
    cursor.execute(f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{database_name1}' AND TABLE_NAME = '{outputname_userinput}child';")
    result = cursor.fetchall()
    if result == () or result == None: 
        print(f"No such child table exists.")
        print(f"Will create [{database_name1}.{outputname_userinput}child] table after sentiment analysis")
        exists_childtable = False
    else:
        print(result)
        print(f"child table exists.. [{database_name1}.{outputname_userinput}child] table")
        exists_childtable = True


    ### 1
    new_ref_number = 0
    #select parenttable_id from result_all_child order by parenttable_id desc limit 1;


    #xxx 1
    if exists_database == False and exists_parenttable == False and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0
        

        #deleteandrename = ok, must implement
        #step 1: create the database, parent, and child table (3 things)
        #step 2: then add new entries (usually parenttable_id/new ref number = 1)
    
    #0xx 2
    if exists_database == True and exists_parenttable == False and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0
        

        #deleteandrename = ok, must implement
        #step 1: create parent and child table (2 things)
        #step 2: then add new entries (usually parenttable_id/new ref number = 1)
        

    #0x0 2
    if exists_database == True and exists_parenttable == False and exists_childtable == True:
        #preparevariables1 = ok
        #step 0: get latest/highest parenttable_id from child table for ref number
        sql = f"select parenttable_id from {database_name1}.{outputname_userinput}child order by parenttable_id ASC;"
        cursor.execute(sql)

        result = cursor.fetchall()
        # pprint.pprint(result)
        #turn into list
        list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
        # remove duplicates
        list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
        print(list_existingoutputfiles1)

        new_ref_number = list_existingoutputfiles1[-1]


        #deleteandrename = ok, must implement
        #step 1: create parent table (1 thing)
        #step 2: delete excessive entries - refer to side programs
        #step 3: rename leftover entries - refer to side programs
        #step 4: then add new entries

        
    #00x 3
    if exists_database == True and exists_parenttable == True and exists_childtable == False:
        #preparevariables1 = ok
        #step 0: set ref number as 0 (+ 1)
        new_ref_number = 0


        #deleteandrename = ok, must implement
        #step 1: clear parent table, create child table (2 things)
        #step 2: then add new entries (usually parenttable_id/new ref number = 1)

    #000 2
    if exists_database == True and exists_parenttable == True and exists_childtable == True:
        #preparevariables1 = ok
        #step 0: get latest/highest parenttable_id from child table for ref number
        sql = f"select parenttable_id from {database_name1}.{outputname_userinput}child order by parenttable_id ASC;"
        cursor.execute(sql)

        result = cursor.fetchall()
        # pprint.pprint(result)
        #turn into list
        list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
        # remove duplicates
        list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
        print(list_existingoutputfiles1)

        new_ref_number = list_existingoutputfiles1[-1]


        #deleteandrename = ok, must implement
        #step 1: delete excessive entries - refer to side programs
        #step 2: rename leftover entries - refer to side programs
        #step 3: then add new entries
    

    ### 3
    if new_ref_number >= max_output_amount:
        print(f'limiting new_ref_number from {new_ref_number} to {max_output_amount}')
        new_ref_number = max_output_amount
    else:
        new_ref_number += 1

    print("new_ref_number set as", new_ref_number)
    print('prepare_variables1_sql_onetableversion()*************************\n')
    return new_ref_number


with connection.cursor() as cursor:
    new_ref_number = prepare_variables1_sql_onetableversion(outputname_userinput, max_output_amount)
print('new_ref_number set as', new_ref_number)

# with connection.cursor() as cursor:
#     print("\nchild table: add new mysql row):")
#     sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     # pprint.pprint(result)
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)

#     while True:
#         if len(list_existingoutputfiles1) >= max_output_amount:           
#             #delete first rows - sql
#             cursor.execute(f"DELETE FROM {database_name1}.{table_name1_child} where parenttable_id = {list_existingoutputfiles1[0]};")

#             #reinitialize list of tables - sql
#             list_existingoutputfiles1 = []
#             sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#             cursor.execute(sql)

#             result = cursor.fetchall()
#             #turn into list
#             list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#             # remove duplicates
#             list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#             print(list_existingoutputfiles1)
                
#         else:
#             break

#     print('renaming leftover rows')
#     for a in list_existingoutputfiles1:
#         new_parenttable_id = list_existingoutputfiles1.index(a) + 1 #adjust from 0 to 1
#         #old_parenttable_id = a
#         sql = f"UPDATE {database_name1}.{table_name1_child} SET parenttable_id = {new_parenttable_id} where parenttable_id = {a};"
#         cursor.execute(sql)
    
#     #reinitialize list of tables - sql
#     list_existingoutputfiles1 = []
#     sql = f"select parenttable_id from {database_name1}.{table_name1_child} order by parenttable_id ASC;"
#     cursor.execute(sql)

#     result = cursor.fetchall()
#     #turn into list
#     list_existingoutputfiles1 = [list(a.values())[0] for a in result] 
#     # remove duplicates
#     list_existingoutputfiles1 = list(dict.fromkeys(list_existingoutputfiles1))
#     print(list_existingoutputfiles1)