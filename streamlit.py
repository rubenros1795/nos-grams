import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from functions import *
import datetime

st.sidebar.title('NOS.nl Unigram Viewer')

ngram_input = st.sidebar.text_input("Ngram (separated by ,)")
rolling_input = st.sidebar.text_input('Rolling Window Size ("0" to ignore)')
relative_input = st.sidebar.checkbox('Relative Frequency')

start_date = st.sidebar.date_input('Start date', datetime.date(2010, 1, 1))
end_date = st.sidebar.date_input('End date', datetime.date(2020, 5, 1))

button_execute = st.sidebar.button('Run!')

with open('resources/totals.json','r') as f:
    totals = json.load(f)

if ngram_input and button_execute:

    # Ngram processing
    ngram_input = ngram_input.split(',')
    regular_ngrams = [x for x in ngram_input if "*" not in x]
    substring_ngrams = [x for x in ngram_input if "*" in x]

    if len(substring_ngrams) > 0:
        vocab = set(pd.read_csv('resources/unique_terms.csv')['w'].tolist())

        substring_matches = []
        for substring in substring_ngrams:
            if substring[0] == '*':
                substring_matches = [w for w in vocab if str(w).endswith(substring.replace('*',''))]
            if substring[-1] == "*":
                substring_matches = [w for w in vocab if str(w).startswith(substring.replace('*',''))]
        regular_ngrams += substring_matches

    st.sidebar.write("Found",len(regular_ngrams),"ngrams")
    ngram_input_split = ["w=" + e.strip() for e in regular_ngrams]

    if len(ngram_input_split) > 10:
        st.sidebar.write("You have many results. For visibility reduce number of ngrams.")
        split_list = [" or ".join(ngram_input_split[i:i + 10]) for i in range(0, len(ngram_input_split), 10)]
        df_list = []

        for sl in split_list:
            df_list.append(pd.read_hdf("ngrams-compressed/1grams.h5",'unigrams',where=sl))
        
        df = pd.concat(df_list,axis=0).reset_index(drop=True)
        
    else:
        ngram_input = " or ".join(ngram_input_split)
        df = pd.read_hdf("ngrams-compressed/1grams.h5",'unigrams',where=ngram_input)
    
    # Data wrangling
    df = df.groupby(['w','m']).sum().reset_index()
    df = df.pivot(index='m',columns='w',values='freq').reset_index().fillna(0)

    all_dates = date_generator('month','2010-01','2021-05')
    all_dates = [d for d in all_dates if d not in df['m']]
    all_dates = pd.DataFrame([[d] + [0 for x in range(len(ngram_input_split))] for d in all_dates],columns=df.columns)
    df = df.append(all_dates)
    df = df.groupby('m').sum().reset_index().sort_values('m',ascending=True).reset_index(drop=True)
    df['m'] =  pd.to_datetime(df['m'], format='%Y-%m')

    st.subheader('Frequency')
    df = pd.melt(df,id_vars='m')
    
    if relative_input:
        df['month'] = [x[:7] for x in df['m'].astype(str)]
        df['value'] = [i / totals[df['month'][c]] for c,i in enumerate(df['value'])]
        df = df.drop('month',axis=1)

    

    if rolling_input != None and rolling_input != "0":
        df = df.pivot(index='m',columns='w',values='value').reset_index()
        for c in list(df.columns)[1:]:
            df[c] = df[c].rolling(int(rolling_input), win_type='gaussian').sum(std=int(rolling_input))
        df = pd.melt(df,id_vars='m')

    if start_date < end_date:
        df['m'] = df['m'].astype('datetime64[ns]')
        start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')

        df = df[(df['m']>start_date) & (df['m']<end_date)]  

    if len(substring_ngrams) > 0:
        dfp = df.pivot(index='m',columns='w',values='value').reset_index()
        st.subheader("Your Results:")
        st.write(", ".join([x.replace('*','') for x in list(dfp.columns)[1:]]))
    try:
        df.columns = ["Periode 2010-2020","Ngram","Frequentie"]
    except Exception as e:
        st.error("Something went wrong. Perhaps your ngram is not in the data. Reload the page to quickly start over!")
    
    bar = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Periode 2010-2020:O", timeUnit="yearmonth", axis=alt.Axis(format="%Y-%m")),
        y='Frequentie',
        color=alt.Color('Ngram', scale=alt.Scale(scheme='tableau20')),
    ).properties(width=1000,height=300).configure_axis(grid=True)

    st.altair_chart(bar, use_container_width=True)
