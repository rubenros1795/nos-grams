
# %%
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


# %%
list_files = gb('html/*')


# %%
def parse_soup(fn):
    with open(fn,'r') as f:
        c = f.read()
    return bs(c)

def parse_metadata(soup):

    metadata = {}
    elements = [x.text for x in s.find_all('span') if '•' in x.text and len(x.text) != 1]
    elements = [x.replace('• ','') for x in elements]
    elements = [x.replace('\n','') for x in elements]
    category = [x for x in elements if x.isdigit() == False][0].split(' •')
    category = [x[:-1] if x[-1] == ' ' else x for x in category]
    
    metadata['categories'] = category

    dates = [x for x in elements if any(i.isdigit() for i in x) == True]

    if len(dates) == 2:
        date_edit = [x for x in dates if 'gepast' in x][0]
        date_edit = date_edit.replace('Aangepast','').replace('• ','').replace('\t','')
        date_or = [x for x in dates if 'gepast' not in x][0]

        metadata['date'] = date_or
        metadata['date_edited'] = date_edit[11:]
    else:
        metadata['date'] = dates[0]
        metadata['date_edited'] = None

    metadata['title'] = soup.find('h1').text.replace('\n','').lstrip()
    return metadata

def find_pars(soup):
    return [x.text.replace('\xa0',' ') for x in s.find_all('p') if 'text' in x.attrs['class'][0] or 'heading' in x.attrs['class'][0]]


# %%
d = {}
for i in tqdm(list_files):
    s = parse_soup(i)
    try:
        metadata = parse_metadata(s)
        # paragraphs = find_pars(s)
        d[i] = metadata
    except:
        continue


# %%
with open('metadata.json','w') as f:
    json.dump(d,f)


