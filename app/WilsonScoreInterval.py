#!/usr/bin/env python
"""
WilsonScoreInterval.py
First Author:  G. Carminati
Calculates the Wilson Score for all the stylists in each salon
"""
import numpy as np
from math import sqrt

from app import load_db

# for each single review rating, calculate weights 
# return 2 values: positive weight, negative weight
def scores(star):
    if star == 1: 
        pos = 0
        neg = 1
    elif star == 2: 
        pos = 0.25 
        neg = 0.75
    elif star == 3: 
        pos = neg = 0.5
    elif star == 4: 
        pos = 0.75 
        neg = 0.25
    elif star == 5: 
        pos = 1 
        neg = 0
    return (pos, neg)


# for each stylist, calculate the sum of weights for each review
# return 2 values: sum(positive weights), sum(negative weights)
def wee(review_star):
    w_up = []
    w_down = []
    for w in range(0,len(review_star)):
        a,b = scores(review_star[w])
        w_up.append(a)
        w_down.append(b)
    print
    return sum(w_up), sum(w_down)

# for each stylist, calculate the lower bound of the Wilson Score confidence 
# interval at 95% confidence
def confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.96 # 1.0 = 65%#1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

def WilsonScore(stylist,business_id):
    cnx = load_db.DB()

    query_review = "SELECT stars FROM review_Vegas_onlyhair WHERE business_id = '" + str(business_id) + "' AND text LIKE '%" + stylist + "%';" 
    cnx.cur.execute(query_review)
    raw3 = cnx.cur.fetchall()
    review_star = [int(row[0]) for row in raw3]
    ups, downs = wee(review_star)
    cnx.cur.close()
    return 1 + 4*(confidence(ups, downs))
