#!/usr/bin/env python
"""
jsonOpen.py
First Author:  P. Phelps
Second Author: G. Carminati
Open series json file
"""

import json
import pandas as pd
import numpy as np
from pprint import pprint
import pdb

def jsonOpen(filename):
    with open(filename) as f:
        for line in f:
            df = pd.DataFrame(json.loads(line) for line in f)
    return df

def main():
    df = jsonOpen()
    #pprint(df)
    #pdb.set_trace()

if __name__ == '__main__':
	main()
