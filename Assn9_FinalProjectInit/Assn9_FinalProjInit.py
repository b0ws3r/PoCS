# For sending GET requests from the API
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
from matplotlib import pyplot as plt


from Monktools import ranktools, statstools, plottools
from TwitterHttpService import *


def clean_word(word):
    word.strip().strip("\"").strip()
    word.strip('"')
    word.replace('"', '')
    word.replace('.', '')
    word.replace(',', '')
    word.replace(';', '')
    word.replace('\'', '')
    word.replace('!', '')
    word.replace('?', '')
    word.replace('*', '')
    word.replace(')', '')
    word.replace('(', '')
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


def send_request(url):
    bearer_token = auth()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    return json_response


def send_request_paginated(url, filename):
    total_tweets = 0
    bearer_token = auth()
    headers = create_headers(bearer_token)
    # Inputs
    count = 0  # Counting tweets per time period
    max_count = 500  # Max tweets per time period
    flag = True
    next_token = None
    # Check if flag is true
    while flag:
        # Check if max_count reached
        if count >= max_count:
            break
        print("-------------------")
        print("Token: ", next_token)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)
            if result_count is not None and result_count > 0 and next_token is not None:
                # print("Start Date: ", start_list[i])
                append_to_csv(json_response, filename)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)
                # If no next token exists
        else:
            if result_count is not None and result_count > 0:
                print("-------------------")
                # print("Start Date: ", start_list[i])
                append_to_csv(json_response, filename)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)

            # Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None


def append_to_csv(json_response, filename):
    # A counter variable
    counter = 0

    # Open OR create the target CSV file
    csv_file = open(filename, "a", newline="", encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    # Loop through each tweet
    for tweet in json_response['data']:

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Geolocation
        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else:
            geo = " "

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']

        # Assemble all data in a list
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source,
               text]

        # Append the result to the CSV file
        csv_writer.writerow(res)
        counter += 1

    # When done, close the CSV file
    csv_file.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter)


def create_csv(filename):
    # Create file
    csvFile = open(filename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    # Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(
        ['author id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
         'source', 'tweet'])
    csvFile.close()
    # append_to_csv(json_response, csvFile.name)


def write_tweets_to_csv(json_response):
    # Create file
    csvFile = open(f"data_{search_term}.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    # Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(
        ['author id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
         'source', 'tweet'])
    csvFile.close()
    append_to_csv(json_response, csvFile.name)


def get_tweets_and_write_to_file(search_term, keyword, start_time, end_time, max_results):
    # query based on parameters for recent tweets
    url = create_url_recent(keyword, start_time, end_time, max_results)
    # json_response = send_request(url)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    filename = f"data_{search_term}.csv"
    create_csv(filename)
    send_request_paginated(url, filename)
    # write results to CSV
    # write_tweets_to_csv(json_response) # this only applies if we're not paginating


# query params:
search_term = "climate"
keyword = f"{search_term} lang:en"
start_time = "2021-10-23T00:00:00.000Z"
end_time = "2021-10-27T00:00:00.000Z"
max_results = 100
get_tweets_and_write_to_file(search_term, keyword, start_time, end_time, max_results)

# now load 'tweet' column and parse out words
df = statstools.get_dataframe(f"data_{search_term}.csv")
tweets = df['tweet']
twitter_words = read_tweets(tweets)
df_raw_tweet_words = pd.DataFrame(twitter_words, columns=["word"])
df_raw_tweet_words.to_csv(f"twitter_raw_words_search={search_term}.csv", index=False)

words_with_freqs = ranktools.group_data(df_raw_tweet_words, 'word', 'k')
n_k = ranktools.group_data(words_with_freqs, 'k', 'N')

fig, ax = plt.subplots()
x_vals, log_nk = ranktools.plot_zipf(ax, list(n_k['N']), 'C0', f'Twitter Zipf based on search term {search_term}')
# plt.show()
plt.savefig(f'Plots/zipf_{search_term}')

# make a word cloud
text = " ".join(words for words in df_raw_tweet_words['word'].astype(str))
wordcloud = WordCloud(stopwords = set(STOPWORDS), max_font_size=50, max_words=100, background_color="white").generate(text)
wordcloud.to_file("Plots/first_review.png")

# all
# url = create_url_all(keyword, start_time, end_time, max_results)
# json_response = send_request(url)

