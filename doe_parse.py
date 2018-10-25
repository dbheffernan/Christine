# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import re
import math

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import Levenshtein as lv
from collections import Counter
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

returns_dict = {
        'party': re.compile(r'(?P<party>.*); ; ; ; ;'),
        'office': re.compile(r'(?P<office>.*); ;'),
        'candidate': re.compile(r'(?P<candidate>.*);'),
        'state' : re.compile(r'State Office - (?P<state>.*)'),
        'nc': re.compile(r'County Office - New Castle County - (?P<nc>.*)'),
        'kc': re.compile(r'County Office - Kent County - (?P<kc>.*)'),
        'sc': re.compile(r'County Office - Sussex County - (?P<sc>.*)')
        }

def _parse_line(line):
    for key, rx in returns_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None
def parser(filepath):
    data = []
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
                key, match = _parse_line(line)
                if key == 'party':
                    party = match.group('party').strip()
                    if(party == 'DEMOCRATIC PARTY'):
                        party = 'D'
                    elif party == 'REPUBLICAN PARTY' :
                        party = 'R'
                    else:
                        party = 'O'
                elif key == 'office':
                    office = line.strip().split(';')
                    office = office[0].strip()
                    print(office)
                    '''if ("county" in office.lower() or "sheriff" in office.lower() or "deeds" in office.lower() or "wills" in office.lower() or "peace" in office.lower()):
                     ''   x = input('County?')
                     ''   office = office + ' ('+ x + ')'
                    ''if ("levy") in office.lower():
                        office = office + ' (K)' 
                    if ("UNITED STATES SENATOR") in office:
                        x = input('Senate Class?')
                        office = office + ' (CLASS ' + str(x) + ')' '''
                else:
                     candidate = line.strip().split(';')
                     name = candidate[0].strip()
                     if name[0] == '*':
                         name = name.split('*')
                         name = name[1].strip()
                     machine = candidate[1].strip()
                     absentee = candidate[2].strip()
                     total = candidate[3].strip()
                     per = candidate[4].strip().split('%')
                     cent = per[0]
                     row = {
                             'Office': office,
                             'Party': party,
                             'Name': name,
                             'Machine': machine,
                             'Absentee': absentee,
                             'Total': total,
                             'Percent': cent,
                             'Won': 0,
                             'Incumbent': 0
                             }
                     data.append(row)
                line = file_object.readline()
            
    data = pd.DataFrame.from_dict(data)
    return data


    


