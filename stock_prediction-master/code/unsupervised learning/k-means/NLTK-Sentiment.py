#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json;
from pprint import pprint


# In[6]:


with open('C:/Users/Michael/Desktop/AMZN/171211/news_0000039.json') as f:
    data = json.load(f)


# In[10]:


content = data['text']


# In[12]:


print(content)


# In[22]:


import nltk
nltk.download('vader_lexicon')


# In[23]:


from nltk.sentiment.vader import SentimentIntensityAnalyzer


# In[24]:


sid = SentimentIntensityAnalyzer()


# In[25]:


ss = sid.polarity_scores("Get Amazon.com Inc. alerts: Amazon.com ( NASDAQ AMZN ) traded up $15.48 during trading on Friday, hitting $1,176.75.")


# In[28]:


print(ss)


# In[31]:


if ss["compound"] == 0.0:
        print("Neutral")
elif ss["compound"] > 0.0:
        print("Positive")
else:
        print("Negative")
