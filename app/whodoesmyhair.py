info="""Flask view mapping for the WhoDoesMyHair app
     """
__author__ = "giadac"
__date__   = "20140911" # made

from flask import render_template
from flask import request 
from app import app

import numpy as np
from nltk import FreqDist
import pdb
import operator

from app import load_db
cnx = load_db.DB()

import WilsonScoreInterval

#..............................................................................
# Main
@app.route('/')
@app.route('/index')
def home():
    """Home authentication page
    """ 
    title = "WhoDoesMyHair"
    return render_template("home.html",title=title,tab="home")

@app.route('/stylist',methods=['POST'])
def result():
    """Stylist
    """ 
    salon = request.form["salonname"]
    title = salon

    cur = cnx.cur

    # query 1:
    # from salon_name get salon_id
    query_id = "SELECT business_id, has_stylists FROM VegasSalonNames WHERE name = '%s'" % salon
    cur.execute(query_id)
    raw = cur.fetchone()
    salon_id = raw[0]
    has_stylist = raw[1]

    # query 2:
    # from salon_id get address, salon_rating, salon_number_of_reviews,
    # stylist_names and salon_number_of_reviews_with_stylist_name
    query = "SELECT full_address, stars, review_count, stylists, review_stylists FROM salonsVegas WHERE business_id = '%s'" % salon_id 
    cur.execute(query)
    raw2 = cur.fetchall()

    # 2.1: format the address info
    address = [ row[0] for row in raw2 ]
    a = str(address[0])
    ad = a.split(",")
    add = sorted(ad)
    location = ""
    street = ""
    city = ""
    for n in add:
        if n.startswith(" NV"): city += "Las Vegas,"+n       
        elif n[0].isdigit(): street = n
        elif n.startswith("Ste"): street += ", "+n
        else: location = n
        
    # 2.2: convert salon_rating in images
    s = [row[1] for row in raw2]
    bsn_stars = float(s[0])

    if   bsn_stars == 1:   imagesrc = "static/images/10stars.png"
    elif bsn_stars == 1.5: imagesrc = "static/images/15stars.png"
    elif bsn_stars == 2:   imagesrc = "static/images/20stars.png"
    elif bsn_stars == 2.5: imagesrc = "static/images/25stars.png"
    elif bsn_stars == 3:   imagesrc = "static/images/30stars.png"
    elif bsn_stars == 3.5: imagesrc = "static/images/35stars.png"
    elif bsn_stars == 4:   imagesrc = "static/images/40stars.png"
    elif bsn_stars == 4.5: imagesrc = "static/images/45stars.png"
    elif bsn_stars == 5:   imagesrc = "static/images/50stars.png"

    # 2.3: extract salon_number_of_reviews
    rc = [row[2] for row in raw2]
    review_count = int(rc[0])

    # ERROR CONTROL:
    # if the business doesn't have a stylist, report an error page
    if not int(has_stylist):
        return render_template("stylist2.html",tab="stylist",
                               from_url="/stylist",salon=salon,
                               street=street,location=location,city=city,
                               bsn_stars=bsn_stars,review_count=review_count,
                               imagesrc=imagesrc)
    else:
        # 2.4: extract stylist_names
        names = [row[3] for row in raw2]
        n = names[0]
        stylists = n.split(" ")
        
        # 2.5: extract salon_number_of_reviews_with_stylist_name
        tr = [row[4] for row in raw2]
        totreviews = float(tr[0])
        
        # 3.1: calculate the highest rated stylists
        fdist = FreqDist(stylists)

        # ERROR CONTROL:
        # we need at least 3 stylists
        if len(fdist) < 4:
            return render_template("stylist2.html",tab="stylist",
                                   from_url="/stylist",salon=salon,
                                   street=street,location=location,
                                   city=city,bsn_stars=bsn_stars,
                                   review_count=review_count,
                                   imagesrc=imagesrc)
        else:
            rating = {}
            for styl in range(0,len(fdist)):
                score = WilsonScoreInterval.WilsonScore(str(fdist.keys()[styl]),salon_id)
                rating[str(fdist.keys()[styl])] = score
                
            hey = sorted(rating.items(),key=operator.itemgetter(1))
            names = [thing[0] for thing in reversed(hey)]
            scores = [str(thing[1])[:4] for thing in reversed(hey)]

    return render_template("stylist.html",tab="stylist",
                           from_url="/stylist",salon=salon,
                           street=street,location=location,city=city,
                           bsn_stars=bsn_stars,review_count=review_count,
                           imagesrc=imagesrc,
                           name0=names[0],score0=scores[0],
                           name1=names[1],score1=scores[1],
                           name2=names[2],score2=scores[2])

@app.route('/slides', methods=["GET"])
def slides():
    """Slides
    """ 
    title = "WhoDoesMyHair demo slides"
    return render_template("slides.html",title=title,tab="slides")

@app.route('/aboutme', methods=["GET"])
def aboutme():
    """Slides
    """ 
    title = "WhoDoesMyHair About Me"
    return render_template("aboutme.html",title=title,tab="aboutme")




