import streamlit as st
from txtSummary import textfunc
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

#extract the subtitle from the video
def textforYT(video_id, no_of_sentences):
    vurl = 'https://www.youtube.com/watch?v=%s' % video_id
    response = requests.get(vurl).text
    title = re.findall(r'"title":"[^>]*",',response)[0].split(',')[0][9:-1]

    a = ytapi.get_transcript(video_id)
    textstr = ""
    for i in a:
        temp = ""
        temp = ' ' + i["text"]
        textstr += temp 
    sent_tokens, word_tokens = tokenize_content(textstr)
    sent_ranks = score_tokens(sent_tokens, word_tokens)
    st.subheader('Summarized Text for YouTube video title: '+title+' ')
    st.write(summarize2(sent_ranks, sent_tokens, no_of_sentences))


def tokenize_content(content):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(content.lower())
    return (sent_tokenize(content), [word for word in words if word not in stop_words])

def score_tokens(sent_tokens, word_tokens):
    word_freq = FreqDist(word_tokens)
    rank = defaultdict(int)
    for i, sent in enumerate(sent_tokens):
        for  word in word_tokenize(sent.lower()):
            if word in word_freq:
                rank[i] += word_freq[word]
    return rank

#base method used to summarize the content
def summarize2(ranks, sentences, length):

    if int(length) > len(sentences):
        st.write('Original Text size is smaller than the requested sentence count')
        return ''

    else:
        indices = nlargest(int(length), ranks, key=ranks.get)
        final_summary = [sentences[j] for j in indices]
        return ' '.join(final_summary)
