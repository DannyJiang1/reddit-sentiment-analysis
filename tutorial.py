import reddit_keys
import pandas as pd
import numpy as np

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

# Now we can read posts from Reddit!

# To read get and read through some posts in a subbredit, run this
for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)
# You can also sort by top, controversial, and more.

submission_df = pd.DataFrame(columns=["SUBMISSION_ID", "Upvote_ratio"])
submission_df.set_index("SUBMISSION_ID")
comment_df = pd.DataFrame(columns=["POST_ID", "COMMENT_ID", "COMMENT_BODY"])
comment_df.set_index("COMMENT_ID")


# A lot of useful information can come from a submission instance
for submission in reddit.subreddit("AmItheAsshole").top(
    time_filter="month", limit=5
):
    # Prints the body of a post
    print(submission.selftext)

    # Prints the ratio of upvotes
    print(submission.upvote_ratio)

    submission_df.loc[submission.id] = [
        submission.upvote_ratio,
        submission.selftext,
    ]

    # Prints each comment
    for comment in submission.comments:
        print(type(comment))
        if type(comment) != praw.models.reddit.more.MoreComments:
            print(comment.body)
            print()

# And there's a lot more that can be done with a submission instance

# Finally let's look at searching by query, rather than by subreddit.
# This will be especially useful for our project, so you can find niche or specific topics.

# First create an instance of a subreddit like previously, but make it of the subreddit "all"
# This indicates we want to search all of reddit for our results
all = reddit.subreddit("all")

# Then simply use the search feature with whatever query you'd like
umich_submissions = all.search("University of Michigan", limit=10)

# Now we can iterate through these posts like before
for submission in umich_submissions:
    print(submission.title)

# You can also search within a subreddit, not just the entirety of Reddit.
# To do so, simply replace "all", with whatever you'd like
tennis = reddit.subreddit("tennis")

tennis_submissions = tennis.search("How do I keep the ball in?", limit=5)

for submission in tennis_submissions:
    print(submission.title)

# That's it for this guide.
# Now, on your own, try messing around with the API and see what information you can gather.
# Refer to this documentation for more ideas https://praw.readthedocs.io/en/stable/index.html
