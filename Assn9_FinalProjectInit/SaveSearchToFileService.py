from datetime import datetime as d1
from datetime import timedelta
import dateutil.parser
from TwitterHttpService import *
import asyncio

DATETIME_RFC3339_STRING = '%Y-%m-%dT%H:%M:%S.000Z'


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
    csvFile = open(filename, "w", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    # Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(
        ['author id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
         'source', 'tweet'])
    csvFile.close()


def write_tweets_to_csv(search_term, json_response):
    # Create file
    csvFile = open(f"{get_filename_based_on_search(search_term)} .csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    # Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(
        ['author id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
         'source', 'tweet'])
    csvFile.close()
    append_to_csv(json_response, csvFile.name)


def get_tweets_and_write_to_file_paginated(search_term, start_time, end_time, max_results):
    # query based on parameters for recent tweets
    keyword = f"{search_term} lang:en"
    url = create_url_recent(keyword, start_time, end_time, max_results)
    filename = get_filename_based_on_search(search_term)
    create_csv(filename)
    send_request_paginated(url, filename)
    return filename


def get_filename_based_on_search(search_term):
    return f"Data/data_{search_term}_{d1.now().strftime('%Y%m%dTH')}.csv"


def send_request_and_write_to_file(search_term, start_time, end_time, max_results):
    # query based on parameters for recent tweets
    keyword = f"{search_term} lang:en"
    url = create_url_recent(keyword, start_time, end_time, max_results)
    json_response = send_request(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    filename = get_filename_based_on_search(search_term)
    create_csv(filename)
    # write results to CSV
    write_tweets_to_csv(search_term, json_response) # this only applies if we're not paginating


def search_twitter_write_to_csv_async(search_term: str):
    start_time = (d1.now() - timedelta(days=6)).strftime(DATETIME_RFC3339_STRING)
    end_time = d1.now().strftime(DATETIME_RFC3339_STRING)
    max_results = 100
    filename = get_tweets_and_write_to_file_paginated(search_term, start_time, end_time, max_results)
    return filename


