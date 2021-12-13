import json
import os
from datetime import datetime as d1
from matplotlib import pyplot as plt

from FinalProject_ClimateChangeLanguage import FollowersToFileService
from Monktools import ranktools, statstools, plottools
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import SaveSearchToFileService
import asyncio


def clean_word(word):
    word.strip('"')
    word.replace('"', '')
    word.replace('.', ' ')
    word.replace(',', ' ')
    word.replace(';', ' ')
    word.replace('\'', '')
    word.replace('!', '')
    word.replace('?', '')
    word.replace('*', '')
    word.replace(')', ' ')
    word.replace('(', ' ')
    word.strip().strip("\"").strip()
    return word


def clean_and_collect_words(line_of_text):
    words = line_of_text.split(" ")
    words = list(map(lambda w: clean_word(w), words))

    return words


def read_tweets(tweets):
    words_in_tweets = []
    for tweet in tweets:
            words_in_tweets = words_in_tweets + clean_and_collect_words(tweet)
    return words_in_tweets

