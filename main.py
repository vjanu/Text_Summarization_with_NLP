import streamlit as st
from txtSummary import textfunc
from ytSummary import textforYT
from newsSummary import summarize
from wikiSummary import wikiSummarize
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
from newspaper import Article
import pyttsx3

def tokenizer(s):
    tokens = []
    for word in s.split(' '):
        tokens.append(word.strip().lower())
    return tokens

def sent_tokenizer(s):
    sents = []
    for sent in s.split('.'):
        sents.append(sent.strip())
    return sents

def count_words(tokens):
    word_counts = {}
    for token in tokens:
        if token not in stop_words and token not in punctuation:
            if token not in word_counts.keys():
                word_counts[token] = 1
            else:
                word_counts[token] += 1
                
    return word_counts

def word_freq_distribution(word_counts):
    freq_dist = {}
    max_freq = max(word_counts.values())
    for word in word_counts.keys():  
        freq_dist[word] = (word_counts[word]/max_freq)
        
    return freq_dist

def score_sentences(sents, freq_dist, max_len=40):
    sent_scores = {}  
    for sent in sents:
        words = sent.split(' ')
        for word in words:
            if word.lower() in freq_dist.keys():
                if len(words) < max_len:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = freq_dist[word.lower()]
                    else:
                        sent_scores[sent] += freq_dist[word.lower()]
                        
    return sent_scores

st.title('Text Summarization using NLP')
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('<center> <h1>Intro to AI:COMP-8700</h1></center>',unsafe_allow_html=True)
image = Image.open('bg1.png')
st.sidebar.image(image, use_column_width=True)

st.sidebar.markdown('<center> Summarizes News Articles, Wikipedia Articles, YouTube Captions and Plain Text</center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h2>Team: AnyTime AI</h2></center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h5>Viraj Wickramasinghe</h5></center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h5>Mohammed Zubair Ahmed</h5></center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h5>Veera Venkata Bharat Kumar Vayitla</h5></center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h5>Dharani Priya Ravi</h5></center>',unsafe_allow_html=True)
st.sidebar.markdown('<center> <h4>Presented to: Prof. Dan Wu</h4></center>',unsafe_allow_html=True)

url = st.text_input('\nProvide the URL of a News Article: ')
txtArticle = st.text_area('\nProvide the Article or Paragraph you want to summarize: ',height=300)
wikiurl = st.text_input('\nProvide the URL of Wikipedia: ')
video_id = st.text_input("\nProvide the Youtube Video Id: ")
no_of_sentences = st.number_input('Choose the no. of sentences/words for the summary: ', min_value = 1)

if video_id and no_of_sentences and st.button('Summarize YouTube Video'):
    if not str(no_of_sentences).isdigit():
        st.write("Problem occured Summarizing the YouTube video!")
    else:
        textforYT(video_id, no_of_sentences)

if txtArticle and no_of_sentences and st.button('Summarize Text/Article'):
    if not str(no_of_sentences).isdigit():
        st.write("Problem occured Summarizing the Article!")
    else:
        textfunc(txtArticle, no_of_sentences)

if url and no_of_sentences and st.button('Summarize News Article'):
    text = ""
    article = Article(url)
    article.download()
    article.parse()
    nltk.download('punkt')

    text = article.text
  
            
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    st.subheader('Original text: ')
    st.write(text)
    
    tokens = tokenizer(text)
    sents = sent_tokenizer(text)
    word_counts = count_words(tokens)
    freq_dist = word_freq_distribution(word_counts)
    sent_scores = score_sentences(sents, freq_dist)
    summary, summary_sent_scores = summarize(sent_scores, no_of_sentences)
    
    st.subheader('Summarized Text: ')
    st.write(summary)
    
    subh = 'Summary sentence score for the top ' + str(no_of_sentences) + ' sentences: '

    st.subheader(subh)
    
    data = []

    for score in summary_sent_scores: 
        data.append([score[1], score[0]])
        
    df = pd.DataFrame(data, columns = ['Sentence', 'Score'])

    st.table(df)

if wikiurl and no_of_sentences and st.button('Summarize WikiPedia Page'):
        wikiSummarize(wikiurl, int(no_of_sentences))

