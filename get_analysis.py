#!/usr/bin/env python
# coding: utf-8

# In[44]:


import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import re
import pandas as pd
import random
from collections import Counter

from tripadvisor_reviews_scraper import get_reviews_from_url


# In[41]:


# pip install -U textblob


# In[52]:


import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

from gensim.parsing.preprocessing import strip_punctuation, strip_numeric,                    strip_non_alphanum, strip_multiple_whitespaces, strip_short

nltk.download('omw-1.4')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from googletrans import Translator
from textblob import TextBlob


# In[ ]:


# if not installed yet, execute
# pip install googletrans==3.1.0a0 
# pip install gensim


# In[367]:


def clean_text(text, name):

    text = text.lower()
    text = re.sub(r'http\S+', '', text) # Remove links
    text = re.sub(r'<.*?>', '', text) # Remove HTML tags
    
    # Remove emoticons
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # text = text.replace(name.lower(), " ") # Remove the name of restaurant
    for n in name.lower().split():
        text = text.replace(n, "")
        
    text = translator.translate(text, dest='en').text # translation to english
    
    text = strip_punctuation(text) # Remove punctuation
    text = strip_non_alphanum(text) # Remove non alphanumeric characters
    text = re.sub(r'\d', '', text) # Remove numbers
    text = re.sub(r'(!)1+', '', text) # remove repetitions
    text = strip_multiple_whitespaces(text) # Remove multiple whitespaces
    
    text = [word for word in text.split() if word not in stopwords and len(word) > 2] # Remove stopwords
    text = [wordnet_lemmatizer.lemmatize(word) for word in text] # lemmatize
    text = " ".join(text)

    return text 


# In[368]:


def get_sentiment(x):
    sentiment = TextBlob(x)
    return sentiment.sentiment.polarity


# In[380]:


# Unique function that given a dataframe does everything you need so you can import to the main

def get_analysis_from_opinions(opinions, name):
    
    df = pd.DataFrame(opinions, columns = ['content'])
    
    df['cleaned'] = df['content'].apply(lambda row: clean_text(row, name))
    
    df = df.replace(r'^s*$', float('NaN'), regex = True) # substitute with empty with NaN
    df.dropna(subset = ['cleaned'], inplace = True) # remove empty rows
    
    df['sentiment'] = df.apply(lambda row: get_sentiment(row.cleaned), axis=1)
    
    # Create three Counter objects to store positive, negative and total counts
    positive_counts = Counter()
    negative_counts = Counter()
    total_counts = Counter()
    
    for idx, row in df.iterrows():
        for word in row['cleaned'].split(" "):
            if(row['sentiment'] > 0):
                positive_counts[word]+=1
            elif (row['sentiment'] < 0):
                negative_counts[word]+=1
            else:
                break
            total_counts[word]+=1
            
    # extract the keys and values from the counter
    max_words = 10
    pos_words = [x[0] for x in positive_counts.most_common()[:max_words]]
    pos_counts = [x[1] for x in positive_counts.most_common()[:max_words]]

    neg_words = [x[0] for x in negative_counts.most_common()[:max_words]]
    neg_counts = [x[1] for x in negative_counts.most_common()[:max_words]]

    max_words_pos = len(pos_words)
    max_words_neg = len(neg_words)

    random.seed(1)
    random.shuffle(pos_words)
    random.shuffle(pos_counts)
    random.shuffle(neg_words)
    random.shuffle(neg_counts)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Sentiment associated to Features')

    if(max_words_pos):
        ax1.fill_between(pos_words, 
                     [pos_counts[i]+1 for i in range(0,max_words_pos)], 
                     [pos_counts[i]-1 for i in range(0,max_words_pos)], 
                     alpha=.5, 
                     linewidth=1, 
                     color='g')
        ax1.plot(pos_words, pos_counts, linewidth=2, color='g')
        ax1.set_xlabel("Positive Features")
        ax1.set_ylabel('Score')
        ax1.tick_params(axis='x', labelrotation = 45)

    if(max_words_neg): # to avoid errors if there are no negative opinions
        ax2.fill_between(neg_words, 
                         [neg_counts[i]+1 for i in range(0,max_words_neg)], 
                         [neg_counts[i]-1 for i in range(0,max_words_neg)], 
                         alpha=.5, 
                         linewidth=1, 
                         color='r')
        ax2.plot(neg_words, neg_counts, linewidth=2, color='r')
        ax2.set_xlabel("Negative Features")
        ax2.set_ylabel('Score')
        ax2.tick_params(axis='x', labelrotation = 45)

    labels = ['Positive', 'Neutral', 'Negative']
    all_counts = [
        df[df['sentiment']>0].sentiment.count(), # pos
        df[df['sentiment']==0].sentiment.count(), # neutral
        df[df['sentiment']<0].sentiment.count() # neg
    ]
    colors = ['g', 'c', 'r']
    explode = (0.05, 0.05, 0.05)

    ax3.pie(all_counts, colors=colors, labels=labels,
            autopct='%1.1f%%', pctdistance=0.85,
            explode=explode)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax3 = plt.gcf()
    ax3.gca().add_artist(centre_circle)

