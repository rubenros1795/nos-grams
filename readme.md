![alt text](https://github.com/rubenros1795/nos-grams/blob/main/logo.png?raw=true)


NOS-grams is an _n_-gram viewer for the NOS.nl [web archive](https://nos.nl/nieuws/archief). The viewer is accessible as a [Streamlit app](https://share.streamlit.io/rubenros1795/nos-grams/main/app.py)


![alt text](https://github.com/rubenros1795/nos-grams/blob/main/intro.gif?raw=true)
-------------------------------------------------------------------------

### Data :file_folder:

The data concerns _n_-grams generated from online news articles published by the Dutch Broadcasting Foundation ([NOS](http://nos.nl)). The NOS articles stretch back until 2010. The organization officially started several years earlier, but unfortunately this data is [lost](https://www.nrc.nl/nieuws/2018/01/09/archief-nosnl-van-voor-2010-niet-meer-terug-te-vinden-a1587608) (web archivists of all countries - unite!). 

For this project the NOS was contacted. In light of the absence of any replies, I cannot share the raw articles. Only the _n_-grams are saved in ```HDF5``` format. In this way the original article cannot be reproduced. Of course, you're free to scrape the archive yourself. Instructions follow below.

----------------------------------------------------

### Preprocessing :wrench:

The preprocessing pipeline looks as follows:

* Scrape the web archive content in ```.html``` format: ```preprocess/scrape-html.py```.
* Parse the metadata (date, category) ```.html``` files and write to ```resources/metadata.json```.: ```preprocess/parse-html.py```
* Extract titles and text content from the ```.html``` files: ```preprocess/parse-text.py```.
* Preprocess text (lowercase, remove all-digit tokens, tokenize): ```preprocess/preprocess.py```.
* Parse 1-4 grams from text data: ```preprocess/parse-ngrams.py```.\*
* Convert _n_-gram ```.csv``` files to ```.h5``` format for increasing the query speed.
* Calculate total token sizes per month: ```preprocess/calculate-totals.ipynb```.

\* N.B.: _n_-grams are written to ```/ngrams``` which is not in this repo due to the size of the files.

---------------------------------------

### The Streamlit App :computer:

The _n_-grams can be queried through the Streamlit app. [Streamlit](https://streamlit.io/) is a fantastic framework for creating dashboards in Python. This app supports the following features:

* Unigram querying (so far no bigrams and higher).
* Multiple queries.
* Wildcards: search for substrings, for example "\*nieuws" or "buitenland\*".
* Relative frequency.
* Two different visualisation types (bar charts and line charts).
* Rolling averages.
* Date range selection.

If you want to reproduce the app locally (check out the Streamlit [documentation](https://docs.streamlit.io/en/stable/api.html)), run ```streamlit run app.py``` after installing the dependencies with ```requirements.txt``` (```pip install requirements.txt```).

---------------------------------------

### Features to be added :hourglass:
* Bigram/trigram support
* Time series correlation support for finding related terms based on diachronic frequency patterns.
* Collocation support for finding related terms based on word context.
* Faster querying using a remote SQL database.
* Fancy colors.