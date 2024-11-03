import reddit_keys
import pandas as pd
import numpy as np
import preprocess
from datetime import datetime
import json
import praw

from reddit_keys import CLIENT_ID, CLIENT_SECRET

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="my user agent",
)

print(reddit.read_only)

submission_list = []
comment_list = []

def convert_to_df(submissions):
    for submission in submissions:
        temp_submission = {
            "SUBMISSION_TITLE": submission.title,
            "SUBMISSION_ID": submission.id,
            "SUBMISSION_DATE": datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m'),
            "SUBMISSION_BODY": submission.selftext,
            "UPVOTE_RATIO": submission.upvote_ratio,
        }
        submission_list.append(temp_submission)
        num_comments = 0
        for comment in submission.comments:
            if type(comment) != praw.models.reddit.more.MoreComments:
                temp_comment = {
                    "COMMENT_ID": comment.id,
                    "SUBMISSION_ID": submission.id,
                    "COMMENT_BODY": comment.body,
                    "UPVOTE_SCORE": comment.score,
                }
                comment_list.append(temp_comment)
                num_comments += 1
                if (num_comments > 10):
                    break
    submission_df = pd.DataFrame(submission_list)
    submission_df.set_index("SUBMISSION_ID")
    comment_df = pd.DataFrame(comment_list)
    comment_df.set_index("COMMENT_ID")

    return submission_df, comment_df

def merge_submission_comment(submission_df, comment_df):
    merged_df = pd.merge(comment_df, submission_df, on='SUBMISSION_ID', how='left')
    return merged_df

submission_df, comment_df = convert_to_df(
    reddit.subreddit("csMajors+cscareerquestions+ITCareerQuestions").top(time_filter='all', limit=1000)
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

df_to_json(merged_df, "csCareerData.json")

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
