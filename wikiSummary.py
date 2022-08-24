import streamlit as st
from bs4 import BeautifulSoup
import requests

import re
from collections import Counter 
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from youtube_transcript_api import YouTubeTranscriptApi as ytapi
import pandas as pd
import bs4 as bs  
import urllib.request  
from PIL import Image
from gensim.summarization import summarize as su_gs
from gensim.summarization import keywords
from gensim.summarization import mz_keywords
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import os
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
import nltk

def wikiSummarize(url_topull, num_of_words):
    
    scraped_data = urllib.request.urlopen(url_topull)  
    article = scraped_data.read()
    
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:  
        article_text += p.text

    stop_words = set(stopwords.words('english')) 
    keywords = mz_keywords(article_text,scores=True,threshold=0.003)
    keywords_names = []
    for tuples in keywords:
        if tuples[0] not in stop_words: 
            if len(tuples[0]) > 2:
                keywords_names.append(tuples[0])

    
    pre_summary = su_gs(article_text,word_count=num_of_words)
    
    summary = re.sub("[\(\[].*?[\)\]]", "", pre_summary)
    
    print_pretty (summary,keywords_names)

def print_pretty (summary, keywords_names):
    columns = os.get_terminal_size().columns
    
    printable = summary
    st.subheader('Summarized Wikipedia Page: ')
    st.write(printable.center(columns))
    str_keywords_names = str(keywords_names).strip('[]')
    printable2 = str_keywords_names
    st.write('Keywords: ' + printable2.center(columns))


