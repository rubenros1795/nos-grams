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

list_files = gb('html/*')

def parse_soup(fn):
    with open(fn,'r') as f:
        c = f.read()
    return bs(c)


def find_pars(soup):
    return [x.text.replace('\xa0',' ').strip() for x in soup.find_all('p') if 'text' in x.attrs['class'][0] or 'heading' in x.attrs['class'][0]]

def find_title(soup):
    return "[TITLE] " + str(soup.find('h1').text).strip()

def parse(fn):
    soup = parse_soup(fn)
    title = find_title(soup)
    paragraphs = find_pars(soup)

    text = [title] + paragraphs 

    text_fn = fn.replace('html','txt')
    with open(text_fn,'w') as f:
        for t in text:
            f.write(t + ' \n')

with concurrent.futures.ThreadPoolExecutor() as e:
    for u in list_files:
        e.submit(parse, u)