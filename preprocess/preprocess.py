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
import string, re
from unidecode import unidecode

list_files = gb('txt/*')

def preproc(fn):
    with open(fn,'r') as f:
        text = f.readlines()
        text = [x.replace('\n', '') for x in text]
    
    title = text[0].replace('[TITLE] ','')
    text = " ".join(text[1:])

    # remove diacritics
    text = unidecode(text)
    title = unidecode(title)

    # lowercase
    text = text.lower()
    title = title.lower()

    # remove non-alphanumeric
    regex = re.compile('[^a-zA-Z]')
    text = regex.sub(' ', text) 
    title = regex.sub(' ', title) 

    # remove extra spaces
    text = re.sub(' +', ' ',text)
    title = re.sub(' +', ' ',title)

    fn = fn.replace('txt/','preproc/')
    with open(fn,'w') as f:
        f.write(title + "\n")
        f.write(text)

with concurrent.futures.ThreadPoolExecutor() as e:
    for u in list_files:
        e.submit(preproc, u)