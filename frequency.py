import streamlit as st
import pandas as pd
import numpy as np
import json
import altair as alt
from functions import *
import datetime


def load_resources():
    with open('resources/totals.json','r') as f:
        totals = json.load(f)

    vocab = set(pd.read_csv('resources/unique_terms.csv')['w'].tolist())
    return totals,vocab

def frequency(ngram_input,rolling_input,relative_input,viz_type,start_date,end_date):
    ## Load Resources
    totals,vocab = load_resources()
    
    # Ngram processing
    original_input = ngram_input.split(',')
    ngram_input = original_input

    unigrams = [x.strip() for x in ngram_input if "*" not in x and " " not in x]
    bigrams = [x.strip() for x in ngram_input if " " in x and "*" not in x]
    wildcards = [x.strip() for x in ngram_input if "*" in x]

    bigrams = []

    if len(unigrams + bigrams + wildcards) == 0:
        st.write("Please enter a valid query. Currently, only unigrams are supported.")

    # Find ngrams in case of wildcard
    if len(wildcards) > 0:
        vocab = set(pd.read_csv('resources/unique_terms.csv')['w'].tolist())

        substring_matches = []
        for substring in wildcards:
            if substring[0] == '*':
                substring_matches = [w for w in vocab if str(w).endswith(substring.replace('*',''))]
            if substring[-1] == "*":
                substring_matches = [w for w in vocab if str(w).startswith(substring.replace('*',''))]
        unigrams += substring_matches
    
    ngram_input_split = ["w=" + e.strip() for e in unigrams]

    # Data Import

    ## If there are a lot of ngrams
    if len(ngram_input_split) > 10:
        split_list = [" or ".join(ngram_input_split[i:i + 10]) for i in range(0, len(ngram_input_split), 10)]
        df_list = []

        for sl in split_list:
            df_list.append(pd.read_hdf("ngrams-compressed/1grams.h5",'unigrams',where=sl))
        
        df = pd.concat(df_list,axis=0).reset_index(drop=True)
        
    # If max. 10 ngrams
    else:
        ngram_input = " or ".join(ngram_input_split)
        df = pd.read_hdf("ngrams-compressed/1grams.h5",'unigrams',where=ngram_input)
    
    # If bigrams
    if len(bigrams) > 0:
        df_list = []
        for bg in bigrams:
            df_list.append(pd.read_hdf(f"ngrams-compressed/1grams-{bg.strip()[0]}.h5",'bigrams',where=f"w='{bg.strip()}'"))
        dfbg = pd.concat(df_list,axis=0).reset_index(drop=True)

    if len(unigrams) > 0 and len(bigrams) > 0: 
        df = df.append(dfbg)

    if len(unigrams) == 0 and len(bigrams) > 0:
        df = dfbg

    if len(df) == 0:
        st.write("No Results! The ngram is probably not in the data.")
        st.stop()
    # Data wrangling
    all_dates = date_generator('month','2010-01','2021-05')
    missing_dates = [d for d in all_dates if d not in df['m']]
    missing_dates = pd.DataFrame([[0,d,original_input[0].strip()] for d in missing_dates],columns=['freq','m','w'])
    df = df.append(missing_dates)
    df['m'] =  pd.to_datetime(df['m'], format='%Y-%m')


    # Handle Relative Frequency with totals
    if relative_input:
        df['month'] = [x[:7] for x in df['m'].astype(str)]

        relfreq = []
        for i,row in df.iterrows():
            month = row['month']
            rf = row['freq'] / totals[month]
            relfreq.append(rf)
        df['freq'] = relfreq
        df = df.drop('month',axis=1)
    
    df = df.groupby(['w','m']).sum().reset_index()

    # Handle rolling window
    if rolling_input != None and rolling_input != "0" and rolling_input != "":
        rolling_input = int(rolling_input)
        df = df.pivot(index='m',columns='w',values='freq').reset_index()
        word = list(df.columns)[1]
        for c in list(df.columns)[1:]:
            df[c] = df[c].rolling(int(rolling_input), win_type='gaussian').sum(std=int(rolling_input))
        df = pd.melt(df,id_vars='m')
        df = df.rename(columns={"value":"freq"})    
    
    # Date formatting and subsetting
    if start_date < end_date:
        df['m'] = df['m'].astype('datetime64[ns]')
        start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')
        df = df[(df['m']>=start_date) & (df['m']<=end_date)]  

    # Print found substrings
    if len(wildcards) > 0:
        dfp = df.pivot(index='m',columns='w',values='freq').reset_index()
        st.subheader("Your Results:")
        st.write("*Wildcard results:*")
        st.write(", ".join([x.replace('*','') for x in list(dfp.columns)[1:]])[:100] + "...")
    
    df = df.rename(columns={"w": "Ngram", "m": "Period","freq": "Frequency"})
    df['Frequency'] = [x if x != 0.0 else None for x in df['Frequency']]

    ## Print Frequency Plot

    if viz_type == "line":

        bar = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("Period:O", timeUnit="yearmonth", axis=alt.Axis(format="%Y-%m")),
            y='Frequency',
            color=alt.Color('Ngram', scale=alt.Scale(scheme='tableau20')),
            tooltip=['Ngram','Frequency']
        ).properties(width=1000,height=300).configure_axis(grid=True,gridColor='lightgrey')


    if viz_type == "bar":
        bar = alt.Chart(df).mark_bar().encode(
            x=alt.X("Period:O", timeUnit="yearmonth", axis=alt.Axis(format="%Y-%m")),
            y='Frequency',
            color=alt.Color('Ngram', scale=alt.Scale(scheme='tableau20')),
        ).properties(width=1000,height=300).configure_axis(grid=True).configure_view(stroke="transparent")


    bar.configure_legend(
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
        orient='top-right'
    )

    return bar,df
