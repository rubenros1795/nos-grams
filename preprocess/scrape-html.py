from datetime import datetime, timedelta, date
from collections import Counter, OrderedDict
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import pandas as pd
import requests
import argparse
import os

base_url = "https://nos.nl/nieuws/archief/"

## Functions
def day_generator(start_day,end_day):
  dates = [start_day, end_day]
  start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
  return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())
    
def getDailyNews(date):
  url = base_url + date + "/"
  req = requests.get(url,timeout=30)
  s = bs(req.content,features='lxml')
  links = s.findAll('a',href=True)
  links = {x.find('div',{"class":"list-time__title link-hover"}).text:x.attrs['href'] for x in links if 'artikel' in x.attrs['href']}
  return links

def saveHtml(url,date,c):
  if 'https://nos.nl' not in url:
     url = 'https://nos.nl' + url 
  req = requests.get(url)
  s = req.text
  with open(f'/home/ruben/Documents/GitHub/NOSMining/html/{date}-{c}.html','w') as f:
    f.write(s)

### Parser
parser = argparse.ArgumentParser()
parser.add_argument("start", help="start date",type=str)
parser.add_argument("end", help="end date",type=str)

args = parser.parse_args()


list_dates = day_generator(args.start,args.end)


for date_ in list_dates:
    try:
        links = getDailyNews(date_)
        for c,link in enumerate(links.values()):
            print(link)
            saveHtml(link,date_,c)
        
    except Exception as e:
        print(e)
        continue
