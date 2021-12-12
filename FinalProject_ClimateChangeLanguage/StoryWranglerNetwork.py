import pandas as pd
import os

from FinalProject_ClimateChangeLanguage import FollowersToFileService


def clean_file():
    dirtyData = 'MichaelData/Climate Change_2021-10-01_2021-11-01.json'
    with open(dirtyData, 'r') as file:
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('}{"_id":', '},{"_id":')
    filedata = "[{0}]".format(filedata)

    cleanData = 'MichaelData/clean_Climate Change_2021-10-01_2021-11-01.json'
    # Write the file out again
    with open(cleanData, 'w') as file:
      file.write(filedata)
    return cleanData


df = pd.read_json(clean_file(), orient='records')
# We need to get the person with a tweet containing "hoax" with the most followers.
hoax_df = df[df['rt_text'].str.contains('hoax', na=False)]

normalized_hoax_actors_json = hoax_df['actor'].to_json(orient='records')
actors_df = pd.read_json(normalized_hoax_actors_json, orient='records')
actors_df = actors_df.rename(columns={"id": "actor_id"})
normalized_hoax_tweets = pd.concat([hoax_df.reset_index(), actors_df.reset_index()],axis=1)

# get the id of that tweet
print(f"Most followers on a hoax tweet: {max(normalized_hoax_tweets['followersCount'])}")
idx = normalized_hoax_tweets['followersCount'].idxmax()
most_followers = normalized_hoax_tweets.iloc[[idx]]

# gather retweet data
# Save the information about the followers of most retweeted node
tweet_id = most_followers['actor_id'].values[0]
tweet_id = str.replace(tweet_id, 'id:twitter.com:', '')
outputDir = f'TweetNetwork_{tweet_id}'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
request_info = FollowersToFileService.create_get_followers_request_info(tweet_id, outputDir)
FollowersToFileService.send_request_paginated(request_info)
# for each file in the output dir for that user, iterate over followers to get their followers.
# followers_list = all followers in all files for user to string
followers_list = list() # TODO
for follower in followers_list:
    # for each follower, run get_followers req.
    FollowersToFileService.create_get_followers_request_info(follower, outputDir)

# now use all files in directory as an adjacency matrix.
# TODO
