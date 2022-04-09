
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

#select * FROM information_schema.tables where table_schema = "rsa_db";
#select table_name, create_time FROM information_schema.tables where table_schema = "rsa_db";



#UPDATE

''' 
UPDATE helloworld.table1
SET name = 'Alfred', date = '1000-11-01'
WHERE product_id = 1;
'''

#SELECT *
'''
SELECT * from helloworld.result_all_001;
'''

#CREATE TABLE, DELETE TABLE
'''
CREATE TABLE helloworld.result_all_001 (
    ticker TEXT,
    date DATE,
    ticker_id INT AUTO_INCREMENT,
    PRIMARY KEY (ticker_id)
);
'''

'''
DROP TABLE helloworld.result_all_001;
'''

#INSERT INTO

'''
INSERT INTO helloworld.result_all_001 (ticker, date)
VALUES ('AAPL', '3333-11-2');
'''

'''
INSERT INTO helloworld.result_all_001 (ticker, date, ticker_id)
VALUES ('AAPL', '3333-11-2', 6);
'''

'''
INSERT INTO helloworld.result_all_001 (ticker)
VALUES ('AAPL');
'''


#DELETE 
'''
DELETE FROM helloworld.result_all_001 
WHERE ticker_id > 4 AND ticker_id < 100;
'''

#GET LIST/COUNT OF TABLES
'''
SHOW tables FROM helloworld;
'''
#done, see sideprogram1.py
'''
SELECT table_name
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'HELLOWORLD';
'''

'''
#count of tables with name like "%____%"
SELECT COUNT(table_name)
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'HELLOWORLD'
AND table_name like "%result%";
'''

#COUNT tables
'''
SELECT COUNT(table_name)  
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'HELLOWORLD';
'''

#RENAME table
'''
RENAME TABLE table1 TO tablen1;
RENAME TABLE tablen1 TO table1;
'''


#look for database like.. / check if database exists
'''
SELECT SCHEMA_NAME
FROM INFORMATION_SCHEMA.SCHEMATA
WHERE SCHEMA_NAME = 'helloworld';
'''
# database_name1 = 'helloworld2'
# cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name1}';")

# result = cursor.fetchall()
# pprint.pprint(result)

# if result == () or result == None: 
#     print(result, '= None')



#create tables (result001 - result010)



'''
f"CREATE TABLE {database_name1}.{outputname_generated} (Number INT, Symbols TEXT, Mentions INT, marketCap TEXT, latestPric TEXT, changePerc TEXT, peRatio TEXT, companyNam TEXT, PRIMARY KEY (Number));"

CREATE TABLE table1 (tickerId INT, symbol TEXT, mentions INT, marketCap DECIMAL(16,2), latestPrice DECIMAL(16,2), changePercent DECIMAL(16,2), peRatio DECIMAL(16,2), companyName TEXT, tableId INT, PRIMARY KEY (tickerId));

INSERT INTO table1 values(1, 'AAPL', 35, 9333222111.015, 100.905, 30.104, -31.105, 'Apple Company', 10);
INSERT INTO table1 values(2, 'AAPL', 35, 7000222111.015, 200.905, 60.104, -61.105, 'Apple Company2', 10);
INSERT INTO table1 values(3, 'AAPL', 35, 5000222111.015, 200.905, 60.104, NULL, 'Apple Company2', 10);
INSERT INTO table1 values(4, 'AAPL', 35, 5000222111.015, 200.905, 60.104, 'NULL', 'Apple Company2', 10);
INSERT INTO table1 values(6, 'AAPL', 35, 5000222111.015, 200.905, 60.104, NULL, 'Apple Company2', 10);


select * from testtable1;
select analysis_id, symbols, concat("$", format(marketCap, 2)) as marketCap from testtable1;
select analysis_id, symbols, concat("$", format(marketCap, 2)) as marketCap from testtable1 where marketCap < 8333222111;
select analysis_id, symbols, concat(changePerc, '%') as changePerc from testtable1 where changePerc < 31;

select tickerid, symbol, concat("$", format(marketCap, 2)) as marketCap from result_4b_007 where marketCap < 400000000000;
#order by marketcap and show formatted marketcap
select tickerid, symbol, mentions, concat("$", format(marketcap/1000000000, 2), "B") as marketcap, latestprice, changepercent, peratio, companyname, tableid from result_all_rds_020 order by cast(marketcap as decimal(16,2)) DESC;

SELECT 
tickerid, 
symbol, 
latestprice,
concat("$", format(marketCap/1000000000, 2), "B") as marketCap 
FROM result_4b_007 
WHERE marketCap < 400000000000;

'''


