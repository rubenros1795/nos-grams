from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime, timedelta, date
from gensim.models import KeyedVectors
from scipy.cluster.vq import kmeans,vq
from collections import OrderedDict
import matplotlib.pyplot as plt
from collections import Counter
from numpy import vstack,array
from nltk.corpus import stopwords
from polyglot.text import Text
from numpy.random import rand
from glob import glob as gb
import re, string,os,io
from tqdm import tqdm
import seaborn as sns
import pandas as pd
import numpy as np
import subprocess
import itertools
import requests
import polyglot
import string
import json
import numpy
import gensim
import random
import math


def date_generator(format,start,end):
    if format == 'month':
        dates = [start, end]
        start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

    if format == 'week':
        if start.split('-')[0] != end.split('-')[0]:
            weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),53)] 
            weeks += [f"{end.split('-')[0]}-{n}" for n in range(0,int(end.split('-')[1])+1)]
        else:
            weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),int(end.split('-')[1]) + 1)] 
        return [x.replace('-','-0') if len(x) == 6 else x for x in weeks]

    if format == 'day':
        dates = [start, end]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())
