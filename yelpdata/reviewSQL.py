#!/usr/bin/env python
"""
reviewSQL.py
First Author:  G.Carminati
Based on K.Soong Insight tutorial on how to create a database for MySQL
"""

import os
import sys
import pymysql as MySQLdb

import json
import pandas as pd
import pdb
import re

# this establishes the connection to the database
conn = MySQLdb.connect(host='localhost',port=int(3306),user='root',passwd='',db='yelpdb',use_unicode=True,charset="utf8")
x = conn.cursor()

# The review dataset has 8 columns, but I split votes in 3 columns, so 10 columns in total -- the primary key is review_id
x.execute("DROP TABLE IF EXISTS review_tbl")
x.execute("CREATE TABLE review_tbl(review_id VARCHAR(30) PRIMARY KEY, user_id varchar(30), stars varchar(5), date varchar(10), text TEXT, type varchar(12), business_id varchar(30), funny varchar(5), useful varchar(5), cool varchar(5))")

with open('yelp_academic_dataset_review.json') as f:
#with open('pippo.json') as f:
    counter = 0
    for line in f:
        data = json.loads(line)

        # here I ask MySQL to find the unique ID in the table
        fc = 'SELECT review_id FROM review_tbl WHERE review_id=%s'
        x.execute(fc,(data["review_id"],))
        outp = x.fetchall()

        # if it's not found I'll insert it
        if not outp:
            insert = '''
            INSERT into review_tbl (review_id, user_id, stars, date, text, type, business_id, funny, useful, cool )
            VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s )
            '''
            # this sends the command, with a set of variables that I choose
            #pdb.set_trace()
            try:
                x.execute(insert,(data["review_id"],data["user_id"],data["stars"],data["date"],data["text"],data["type"],data["business_id"],data["votes"]['funny'],data["votes"]['useful'],data["votes"]['cool'] ))
            except:
                counter += 1
                continue
        else: # otherwise I won't
            print 'already in table!'
    
# So far everything that's been done is held in a temporary space. Without this command, the changes to the database will disappear once the script finished running
conn.commit()

# close the session when done
x.close()
conn.close()
