import streamlit as st
import pandas as pd
import numpy as np
import tables
import json
import altair as alt
from functions import *
from frequency import * 
from collocation import *
import datetime
import nltk
from nltk.collocations import *
from operator import itemgetter
from glob import glob as gb
import streamlit as st
import streamlit.components.v1 as components


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    # st.beta_set_page_config(layout="wide")
    st.title('NOS.nl *N*-gram Viewer')

    with st.beta_expander("Read more..."):
        st.write("""
            
            ## Welcome!
            This dashboard offers the possibility to plot _n_-gram frequencies. _N_-grams are sequences of words (in case you wondered). This viewer queries the archive of the Dutch national broadcaster NOS. Its web archive goes back until 2010. This viewer contains the _n_-gram data from 2010-01-01 until 2020-12-31. The original data is found on www.nos.nl/archief.
             
            The viewer supports only unigram queries. Wildcards (term\*) are also supported, but note that they can return many results.
            
            Customize your search by date and choose between absolute and relative frequency (frequency of a term shared by the total number of tokens in that month). 
            
            ## Data


            The data is scraped from the web archive and tokenized. Tokens consisting only of digits are removed and all text is lowercased. The data is stored in HDF5 format to speed things up. Please note that despite the compression, querying a lot of terms still takes some time.

            
            The documentation can be found [here](https://github.com/rubenros1795/nos-grams).

            """)


    ## Inputs

    ngram_input = st.text_input("Ngram (separated by ,)")
    
    col1a, col2a, col3a, col4a = st.beta_columns((1,1,1,1))

    viz_type = col1a.selectbox("Visualization type",("bars","lines"))
    rolling_input = col2a.text_input('Rolling Window Size')

    start_date = col3a.date_input('Start date', datetime.date(2010, 1, 1))
    end_date = col4a.date_input('End date', datetime.date(2021, 1, 1))



    relative_input = col1a.checkbox('Relative Frequency')

    ## Execute Button
    button_execute = col4a.button('Run!')

    if ngram_input and button_execute:
        bar,df = frequency(ngram_input,
                rolling_input,
                relative_input,
                viz_type,
                start_date,
                end_date
                )

        alt.renderers.enable(embed_options={'theme': 'urbaninstitute'})
        st.altair_chart(bar, use_container_width=True)
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
