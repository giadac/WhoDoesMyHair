#!/usr/bin/env python
"""
businessSQL.py
First Author:  G.Carminati
Based on K.Soong Insight tutorial on how to create a database for MySQL
"""

import os
import sys
import pymysql as MySQLdb

import json
import pandas as pd
import pdb

# this establishes the connection to the database
conn = MySQLdb.connect(host='localhost',port=int(3306),user='root',passwd='',db='yelpdb')
x = conn.cursor()

# The business dataset has 17 columns, but I'll use only 12 -- the primary key is business_id
x.execute("DROP TABLE IF EXISTS business")
x.execute("CREATE TABLE business(business_id VARCHAR(30) PRIMARY KEY, name varchar(255), full_address varchar(255), city varchar(255), state varchar(255), latitude varchar(255), longitude varchar(255), stars varchar(255), review_count varchar(255), categories varchar(255), open varchar(255), type varchar(255))")

with open('yelp_academic_dataset_business.json') as f:
    for line in f:
        data = json.loads(line)

        # here I ask MySQL to find the unique ID in the table
        fc = 'SELECT business_id FROM business WHERE business_id=%s'
        x.execute(fc,(data["business_id"],))
        outp = x.fetchall()

        # if it's not found I'll insert it
        if not outp:
            insert = '''
            INSERT into business (business_id, name, full_address, city, state, latitude, longitude, stars, review_count, categories, open, type)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            '''
            # this sends the command, with a set of variables that I choose
        #pdb.set_trace()
            x.execute(insert,(data["business_id"],data["name"],",".join(data["full_address"].splitlines()),data["city"],data["state"],data["latitude"],data["longitude"],data["stars"],data["review_count"],",".join(data["categories"]),data["open"],data["type"]))
        else: # otherwise I won't
            print 'already in table!'
    
# So far everything that's been done is held in a temporary space. This command makes it permanent.
# Without this command, the changes to the database will dissapear once the script finished running
conn.commit()

# close the session when done
x.close()
conn.close()
