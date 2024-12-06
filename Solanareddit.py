import praw
import logging
import csv
import os 

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def initialize_reddit(subreddit_name): 
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    user_agent = 'MyRedditApp v1.0'  

    reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
    subreddit = reddit.subreddit(subreddit_name)
    logger.info("Subreddit value is %s",subreddit)

    return subreddit



def fetch_subreddit_data(subreddit, limit):
    logging.info(f"Fetching data from subreddit:   {subreddit}")
    data = []
    for submission in subreddit.top(limit = limit): 
        post_details = {
            "title":submission.title, 
            "author": str(submission.author),
            "url": submission.url,
            'comments': []
        }
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            comment_details = top_level_comment.body
            post_details["comments"].append(comment_details)

        data.append(post_details)
    logging.info(f"Fetched {len(data)} posts from {subreddit}")
    return data




def save_to_csv(data, file_name):
    if data: 
        fieldnames = data[0].keys()
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Data saved to {file_name}")
    else:
        logger.warning("No data to save.")


def main(): 

    subreddit_name = 'solana'
    subreddit = initialize_reddit(subreddit_name)
    posts = fetch_subreddit_data(subreddit, 10)
    save_to_csv(posts, "reddit_solanatop.csv")


if __name__ == main():
    main()