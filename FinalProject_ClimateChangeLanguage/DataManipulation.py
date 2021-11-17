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


##########################################################################
# now load 'tweet' column and parse out words
search_term = "Climate change is a hoax"
outfile = SaveSearchToFileService.search_twitter_write_to_csv_async(search_term)
df = statstools.get_dataframe(outfile)

df.set_index('id')
tweets = df['tweet']
twitter_words = read_tweets(tweets)
df_raw_tweet_words = pd.DataFrame(twitter_words, columns=["word"])
df_raw_tweet_words.to_csv(f"Data/twitter_raw_words_src={search_term}_{d1.now().strftime('%Y%m%d%_H')}.csv", index=False)


##########################################################################
# gather frequencies of words
words_with_freqs = ranktools.group_data(df_raw_tweet_words, 'word', 'k')
n_k = ranktools.group_data(words_with_freqs, 'k', 'N')


##########################################################################
# gather retweet data
print(f" Most retweeted item was retweeted {max(df['retweet_count'])} times. ")
idx = df['retweet_count'].idxmax()
max_retweeted = df.at[idx, 'author id']

# gather retweet data
# Save the information about the followers of most retweeted node
request_info = FollowersToFileService.create_get_followers_request_info(max_retweeted)
FollowersToFileService.send_request_paginated(request_info)


##########################################################################
# plot zipf
fig, ax = plt.subplots()
x_vals, log_nk = ranktools.plot_zipf(ax, list(n_k['N']), 'C0', f'Twitter Zipf based on search term {search_term}')
# plt.show()
plt.savefig(f'Plots/zipf_{search_term}')

##########################################################################
# make a word cloud
text = " ".join(words for words in df_raw_tweet_words['word'].astype(str))
wordcloud = WordCloud(stopwords = set(STOPWORDS), max_font_size=50, max_words=100, background_color="white").generate(text)
wordcloud.to_file("Plots/first_review.png")
