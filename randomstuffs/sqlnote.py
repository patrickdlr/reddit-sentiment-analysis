
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
#select student_id, table1.name, grade, date, table3.product_id, table3.name, ta[ble3.price from table1 join table3 on table1.product_id = table3.product_id;
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
f"CREATE TABLE {database_name1}.{outputname_generated} (Number INT, Symbols TEXT, Mentions INT, market_cap TEXT, latestPric TEXT, changePerc TEXT, pe_ratio TEXT, companyNam TEXT, PRIMARY KEY (Number));"

CREATE TABLE table1 (ticker_id INT, symbol TEXT, mentions INT, market_cap DECIMAL(16,2), latest_price DECIMAL(16,2), change_percent DECIMAL(16,2), pe_ratio DECIMAL(16,2), company_name TEXT, tableId INT, PRIMARY KEY (ticker_id));

INSERT INTO table1 values(1, 'AAPL', 35, 9333222111.015, 100.905, 30.104, -31.105, 'Apple Company', 10);
INSERT INTO table1 values(2, 'AAPL', 35, 7000222111.015, 200.905, 60.104, -61.105, 'Apple Company2', 10);
INSERT INTO table1 values(3, 'AAPL', 35, 5000222111.015, 200.905, 60.104, NULL, 'Apple Company2', 10);
INSERT INTO table1 values(4, 'AAPL', 35, 5000222111.015, 200.905, 60.104, 'NULL', 'Apple Company2', 10);
INSERT INTO table1 values(6, 'AAPL', 35, 5000222111.015, 200.905, 60.104, NULL, 'Apple Company2', 10);


select * from testtable1;
select analysis_id, symbols, concat("$", format(market_cap, 2)) as market_cap from testtable1;
select analysis_id, symbols, concat("$", format(market_cap, 2)) as market_cap from testtable1 where market_cap < 8333222111;
select analysis_id, symbols, concat(changePerc, '%') as changePerc from testtable1 where changePerc < 31;

select tickerid, symbol, concat("$", format(market_cap, 2)) as market_cap from result_4b_007 where market_cap < 400000000000;
#order by marketcap and show formatted marketcap
select tickerid, symbol, mentions, concat("$", format(marketcap/1000000000, 2), "B") as marketcap, latestprice, changepercent, peratio, companyname, tableid from result_all_rds_020 order by cast(marketcap as decimal(16,2)) DESC;

SELECT 
tickerid, 
symbol, 
latestprice,
concat("$", format(market_cap/1000000000, 2), "B") as market_cap 
FROM result_4b_007 
WHERE market_cap < 400000000000;

'''


#########################
#########################
#########################
#########################

'''
###result_all_parent testing:
CREATE TABLE result_all_parent (parenttable_id INT, subreddit_count INT, upvote_ratio DECIMAL(16, 1), ups INT, limit_reddit INT, upvotes INT, picks INT, picks_ayz INT, seconds_took DECIMAL(16, 1), comments_analyzed INT, datetime DATETIME, tickers_found INT, max_market_cap DECIMAL(16, 2));
# ALTER TABLE result_all_parent ADD PRIMARY KEY(parenttable_id);

INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (16, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (15, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (14, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (13, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (12, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (11, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (10, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (9, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (8, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (7, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (6, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (5, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (4, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (3, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (2, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);
INSERT INTO result_all_parent (parenttable_id, subreddit_count, upvote_ratio, ups, limit_reddit, upvotes, picks, picks_ayz, seconds_took, comments_analyzed, datetime, tickers_found, max_market_cap) VALUES (1, 64, 0.5, 20, 1, 2, 100, 100, 800.91, 480, now(), 11796, 4000000000);

#extras:
select * from result_all_parent where datetime like '2022-04-11%';
UPDATE result_all_parent SET parenttable_id = 19 WHERE parenttable_id = 20;
'''


'''
###result_all_child testing:
CREATE TABLE result_all_child (ticker_id INT, symbol TEXT, mentions INT, market_cap DECIMAL(16,2), latest_price DECIMAL(16,2), change_percent DECIMAL(16,2), pe_ratio DECIMAL(16,2), company_name TEXT, datetime DATETIME, parenttable_id INT);
ALTER TABLE result_all_child ADD CONSTRAINT fk_metaandanalysis FOREIGN KEY (parenttable_id) REFERENCES result_all_parent(parenttable_id);

INSERT INTO result_all_child (ticker_id, symbol, mentions, market_cap, latest_price, change_percent, pe_ratio, company_name, datetime, parenttable_id) VALUES (2, 'AAPL', 19, 4333222111.99, 159.109, 99.95, 25.00, 'Apple Co.', now(), 8);
INSERT INTO result_all_child (ticker_id, symbol, mentions, market_cap, latest_price, change_percent, pe_ratio, company_name, datetime, parenttable_id) VALUES (2, 'AAPL', 19, 4333222111.99, 159.109, 99.95, 25.00, 'Apple Co.', now(), 7);

#extras:
DELETE FROM result_all_child where parenttable_id = 19;
UPDATE result_all_child set parenttable_id = 20; #sets all data under parenttable_id column to 20;


###using one childtable and one parenttable... to get meta data for a table/batch of tickers by parenttable_id = ok
SELECT * FROM result_all_parent where parenttable_id = 19; #final
SELECT * FROM result_all_parent where parenttable_id = 20; #final

###using one childtable and one parenttable... to get a list of tickers with certain parenttable_id and certain tickerids
# SELECT c1.* FROM result_all_parent m1 JOIN result_all_child c1 WHERE c1.parenttable_id = m1.parenttable_id AND m1.parenttable_id = 19 AND c1.tickerid <= 2;
SELECT * FROM result_all_child where parenttable_id = 19; #final
SELECT * FROM result_all_child where parenttable_id = 20; #final
SELECT * FROM result_all_child where parenttable_id = 20 and ticker_id = 1; #final

#try using multiple childtables and one parenttable? ..use filters, like table_name?
Proably too slow and requires Python to loop thru all tables for now.

'''

