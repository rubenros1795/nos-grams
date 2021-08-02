# nos-grams

This repository contains a streamlit app that provides an Ngram viewer for NOS data. The NOS is the Dutch Public Broadcaster and publishes daily news articles since 2010. Their articles offer a unique insight in Dutch (media). 

All articles are scraped, preprocessed and converted into ngrams. The ngrams can be queried and their diachronic frequency is visualized. Multiple searches, rolling windows and wildcards are supported. Currently, the viewer supports only unigrams.

Features to be added:
- bigram/trigram support
- time series correlation support (for finding related terms based on diachronic frequency patterns)
- collocation support (for finding related terms based on word context)
