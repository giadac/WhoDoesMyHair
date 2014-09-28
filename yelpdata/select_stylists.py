#!/usr/bin/env python
"""
select_names.py
First Author:  G. Carminati
Open series json file
"""
import pymysql as mdb
cnx = mdb.connect(host='localhost',port=int(3306),user='root',passwd='',db='yelpdb')
cur = cnx.cursor()

import numpy as np
from nltk import word_tokenize
from nltk import pos_tag
from nltk.tag.stanford import NERTagger

def select_names(cnx,business_id):
    query = "SELECT * FROM hairVegas2 WHERE business_id = '%s' " %business_id
    cur.execute(query)
    raw = cur.fetchall()

    review = [row[4] for row in raw]
    #print type(review)

    unames = {}
    for i in range(0, len(review)):
        r = review[i]
        tokens = word_tokenize(r)
        tagged_token = pos_tag(tokens)
        nouns_only = [ word for (word, tag) in tagged_token if tag.startswith('NNP')]
        nopunct_nouns = [word.replace(".","") for word in nouns_only ]
        st = NERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       '/usr/share/stanford-ner/stanford-ner.jar') 
        persons = st.tag(nopunct_nouns)
        names = [ n for n,p in persons if p == 'PERSON' ]
        unique = list(set(names))
        unames[i] = unique

    for r in range(0, len(review)):
        aset = unames[r]
        for i in range(0, len(aset)):
            for j in range(i+1, len(aset)):
                tokens = word_tokenize(review[r])
                nopunct_tokens = [word.replace(".","") for word in tokens ]
                a = nopunct_tokens.index(aset[i])
                b = nopunct_tokens.index(aset[j])
                #print r, a, b
                if abs(b-a) == 1:
                    if b > a: unames[r].pop(j)
                    else: unames[r].pop(i)

    #print unames
    person = [name for sublist in unames.values() for name in sublist]
    #print person
    return person

if __name__ == '__main__':
    person = select_names(cnx,'24/7 Salon & Day Spa Studio')
    



