import reddit_keys
import pandas as pd
import numpy as np
import preprocess
import json

# The first step is setting up a virtual environment
# Virtual environments are extremely important to writing clean code
# They isolate projects from each other, enhance colloboration, version control, and dependency management

# To set up a virtual environment, first make sure you have Python installed

# If you don't you can install python by doing the following:
# macOS:
# brew install python3
# you can install homebrew here https://brew.sh

# Windows or Linux(who uses Linux??):
# sudo apt-get update
# sudo apt-get install python3 python3-pip python3-venv python3-wheel python3-setuptools

# Now run this command
# python3 -m venv env
# This creates a virtual environment in your working directory

# To activate your env run
# source env/bin/activate
# Now you can safely install packages in your virtual environment!

# From here we have to import the required packages
import praw

# You'll notice this line is giving an error,
# that's because the package hasn't been installed to our virtual environment yet.

# To install praw, run
# pip install praw

# For this project we will only be reading from the Reddit API
# So first we create an instance that can do just that
from reddit_keys import CLIENT_ID, CLIENT_SECRET

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="my user agent",
)
# Go back to your Reddit App page from earlier
# you'll see the client_secret there,
# as well as the client_id, it's located below your application name

# Don't just place those values in the Reddit instance, that's bad practice
# Instead, place them in the reddit_keys.py file, replacing the placeholders with your values
# Then add the import statement "from reddit_keys import CLIENT_ID, CLIENT_SECRET"
# Now you can replace the quotes with those variables
# Practices like these are what allow us to keep private variables out of public repositories

# Double check that your instance is working by running this command
print(reddit.read_only)

submission_list = []
comment_list = []


def convert_to_df(submissions):
    for submission in submissions:
        temp_submission = {
            "SUBMISSION_TITLE": submission.title,
            "SUBMISSION_ID": submission.id,
            "SUBMISSION_BODY": submission.selftext,
            "UPVOTE_RATIO": submission.upvote_ratio,
        }
        submission_list.append(temp_submission)
        for comment in submission.comments:
            if type(comment) != praw.models.reddit.more.MoreComments:
                temp_comment = {
                    "COMMENT_ID": comment.id,
                    "SUBMISSION_ID": submission.id,
                    "COMMENT_BODY": comment.body,
                    "UPVOTE_SCORE": comment.score,
                }
                comment_list.append(temp_comment)
    submission_df = pd.DataFrame(submission_list)
    submission_df.set_index("SUBMISSION_ID")
    comment_df = pd.DataFrame(comment_list)
    comment_df.set_index("COMMENT_ID")

    return submission_df, comment_df

def merge_submission_comment(submission_df, comment_df):
    merged_df = pd.merge(comment_df, submission_df, on='SUBMISSION_ID', how='inner')
    return merged_df

submission_df, comment_df = convert_to_df(
    reddit.subreddit("csMajors+cscareerquestions").hot(limit=5)
)

submission_df["CLEANED_BODY"] = submission_df["SUBMISSION_BODY"].apply(
    # lambda text: preprocess.preprocess(["lower", "expand", "stopwords"], text)
    lambda text: preprocess.preprocess(["expand", "lower", "stopwords"], text)
)

comment_df["CLEANED_BODY"] = comment_df["COMMENT_BODY"].apply(
    # lambda text: preprocess.preprocess(["lower", "expand", "stopwords"], text)
    lambda text: preprocess.preprocess(["expand", "lower", "stopwords"], text)
)

print(submission_df.head())
print(comment_df.head())

merged_df = merge_submission_comment(submission_df, comment_df);

def df_to_json(df, filename):
    df_as_dict = df.to_dict(orient='records')
    with open(filename, 'w') as json_file:
        json.dump(df_as_dict, json_file, indent=4)
    print(f"Data saved as {filename}")

df_to_json(merged_df, "test.json")

# A lot of useful information can come from a submission instance
# # Prints the ratio of upvotes
# print(submission.upvote_ratio)

# submission_df.loc[submission.id] = [
#     submission.upvote_ratio,
#     submission.selftext,
# ]

# Prints each comment

# all = reddit.subreddit("csMajors+cscareerquestions")

# # Then simply use the search feature with whatever query you'd like
# search_submissions = all.search("Major", limit=10)

# # Now we can iterate through these posts like before
# print_submissions(search_submissions)


# That's it for this guide.
# Now, on your own, try messing around with the API and see what information you can gather.
# Refer to this documentation for more ideas https://praw.readthedocs.io/en/stable/index.html
