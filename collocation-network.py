from collections import Counter
import os,re,string,json,math
from tqdm import tqdm
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.collocations import *
from gensim.models.phrases import Phrases
from operator import itemgetter
from glob import glob as gb
from unidecode import unidecode

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


def preproc(text):
    text = unidecode(text)
    text = text.lower()
    regex = re.compile('[^a-zA-Z]')
    text = regex.sub(' ', text) 
    text = re.sub(' +', ' ',text)
    return text

def read_month(month):
    list_files = [t for t in gb('txt/*') if os.path.split(t)[-1].startswith(month)]
    
    texts = []

    for f in list_files:
        with open(f,'r') as f:
            t = f.readlines()
            t = " ".join([x.replace('\n','').replace('[TITLE]','') for x in t])
        texts.append(preproc(t))
    return pd.DataFrame(texts,columns=['text'])

def find_top_collocates(bgfinder, vocabulary, seed_term, topn):
    list_scores = {w:bgfinder.score_ngram(bigram_measures.likelihood_ratio,seed_term,w) for w in vocabulary}
    list_scores = {k:v for k,v in list_scores.items() if v != None}
    return list(dict(sorted(list_scores.items(), key = itemgetter(1), reverse = True)[:topn]).keys())

def get_network(seed_term,bgfinder,vocabulary,topn):
    d = []
    for w1 in find_top_collocates(bgfinder, vocabulary, seed_term,topn):
        d.append([seed_term,w1])
        for w2 in find_top_collocates(bgfinder, vocabulary, w1,topn):
            d.append([w1,w2])
            for w3 in find_top_collocates(bgfinder, vocabulary, w2,topn):
                d.append([w2,w3])
    return pd.DataFrame(d,columns=['source','target'])

def collocation_month(finder,vocab,seed_term,topn=6,degree_limit=0):
    d = get_network(seed_term,finder,vocab,topn)
    g = nx.from_pandas_edgelist(d, source='source', target='target',create_using=nx.DiGraph()) 
    dgrs = dict(g.degree)

    plt.figure(figsize=(25,15))
    layout = nx.spring_layout(g,k=1.15)

    nx.draw_networkx_nodes(g,layout,node_size=2,alpha=0)
    nx.draw_networkx_edges(g, layout, width=1.5, alpha=.75, edge_color="#cccccc",arrows=True,arrowstyle="-|>",arrowsize=50)
    
    for node, (x, y) in layout.items():
        plt.text(x, y, node, fontsize=math.log(dgrs[node] * 5) * 6, ha='center', va='center',color = "red" if node == seed_term else "black",bbox=dict(facecolor='red', alpha=0.1))
    plt.savefig(f'{seed_term}-network.png',dpi=250)    

df_text = read_month('2020-03')
finder = BigramCollocationFinder.from_words(" ".join(df_text['text']).split(' '),window_size=10)
vocab = set(" ".join(df_text['text']).split(' '))

collocation_month(finder,vocab,'corona')