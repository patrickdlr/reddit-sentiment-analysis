import pathlib, os, time, sys
import ast, requests, pprint
import pandas as pd


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
#with connection:
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
   
    # print('\n')
    # with connection.cursor() as cursor:
        
    #     #create new table in target schema/database
    #     table_name = "table4"
    #     table_schema = "helloworld"

        
    #     #check if table exists
    #     sql = f"USE {table_schema}"
    #     cursor.execute(sql)
    #     sql = f"SELECT * FROM information_schema.tables WHERE table_schema = {table_schema} AND table_name = {table_name}"
        
    #     if cursor.execute(sql) == 1: #1 = exists
    #         print(f"table {table_name} already exists")

    #         ###drop table
    #         print(f"deleting {table_name}")
    #         sql2 = f"DROP {table_name}"
    #         cursor.execute(sql2)
        
    #     elif cursor.execute(sql) == 0: #0 = doesn't exist 
            

    #         #create table
    #         print(f"creating {table_name}")
    #         sql2 = f"CREATE TABLE {table_name} (id INT, computer_name TEXT);"
    #         cursor.execute(sql2)
            
        
    #     result = cursor.fetchall()
    #     pprint.pprint(result)  

    


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

cursor = connection.cursor()


def function_sql1():
    cursor.execute("show databases;")
    result = cursor.fetchall()
    pprint.pprint(result)

def function_sql2():
    cursor.execute("select * from helloworld.table1;")
    result = cursor.fetchall()
    pprint.pprint(result)


# function_sql1()
# function_sql2()



# # # check if database exists, create one if doesnt exist
# database_name1 = 'helloworld2'
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