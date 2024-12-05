import praw
import logging
import csv

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client_id = 'Nu0aZu7KI2XJXZAjoFfZxA'  
client_secret = 'puyFoHWLcpS9swGPwCD9lT07V259Vw'  
user_agent = 'MyRedditApp v1.0'  

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

subreddit_name = 'solana'
subreddit = reddit.subreddit(subreddit_name)
print(subreddit)
logger.info("Subreddit value is %s",subreddit)



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

posts = fetch_subreddit_data(subreddit, 10)
print(posts)

csv_file = "reddit_solanatop.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=posts[0].keys())
    writer.writeheader()
    writer.writerows(posts)

print(f"Data saved to {csv_file}")


