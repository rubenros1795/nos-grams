import pandas as pd
from glob import glob as gb 
from bs4 import BeautifulSoup as bs
import random
from tqdm import tqdm
import json
import collections
import pandas as pd
import itertools
import json,sys
import concurrent.futures
import datetime
from collections import Counter

list_files = sorted(gb('preproc/*'))

with open('metadata.json','r') as f:
    metadata = json.load(f)

def get_week(fn):
    date = "-".join(fn[8:-5].split('-')[:-1])
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = str(date.year)
    month = str(date.month)
    week = str(date.isocalendar()[1])
    id_ = f"{year}-W{week}-M{month}"
    return id_

def get_month(fn):
    date = "-".join(fn[8:-5].split('-')[:-1])
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    year = str(date.year)
    month = str(date.month)
    id_ = f"{year}-{month}"
    if len(id_) == 6:
        id_ = id_.replace('-','-0')
    return id_

def ngrams(fn, n):
    with open(fn,'r') as f:
        text = f.readlines()
    if len(text) == 2:
        text = text[1]
        t = zip(*[text.split(' ')[i:] for i in range(n)])
        t = [" ".join(x) for x in list(t)]
        return dict(Counter(t))
    else:
        return {None:0}

############

print("aggregating weeks")
dict_week = {}

for fn in list_files:
    week = get_month(fn)
    if week not in dict_week.keys():
        dict_week.update({week:[fn]})
    else:
        dict_week[week].append(fn)

############

for c in [1,2,3,4]:
    fn_= f"{c}grams"
    print(fn_)

    with open(f'/home/ruben/Documents/GitHub/NOSMining/ngrams/{fn_}.csv','w') as file_:
        file_.write(",".join(['ngram','frequency','relative_frequency','month']) + "\n")
        for week in tqdm(dict_week.keys()):
            
            files_week = dict_week[week]
            dict_counts = {}

            for f in files_week:
                counts = ngrams(f,c)
                for k,v in counts.items():
                    if k in dict_counts.keys():
                        dict_counts[k] += v 
                    else:
                        dict_counts.update({k:v})
            
            sum_ = sum(list(dict_counts.values()))
            dict_counts = {k:v for k,v in dict_counts.items() if k != None}
            for k,v in dict_counts.items():
                if k != None:
                    file_.write(','.join([k,str(v),str(v / sum_),week]) + "\n")
