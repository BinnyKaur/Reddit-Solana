import os
import json
import boto3
from datetime import datetime
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Get credentials and config from environment variables

REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
SUBREDDIT_NAME = os.environ.get('SUBREDDIT_NAME', 'solana')  

analyzer = SentimentIntensityAnalyzer()

def lambda_handler(event, context):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = subreddit.new(limit=10)  

    reddit_data = []

    for post in posts:
        post.comments.replace_more(limit=0)
    
        comments = []
        comment_upvotes = 0
        comment_sentiments = []

        for comment in post.comments.list():
            comments.append(comment.body)
            comment_upvotes += comment.score
            sentiment_score = analyzer.polarity_scores(comment.body)['compound']
            comment_sentiments.append(sentiment_score)

        avg_comment_sentiment = round(sum(comment_sentiments) / len(comment_sentiments), 4) if comment_sentiments else 0.0
        post_sentiment = round(analyzer.polarity_scores(post.title)['compound'], 4)

        reddit_data.append({
            'title': post.title,
            'author': str(post.author),
            'url': post.url,
            'created_utc': post.created_utc,
            'upvotes': post.score,
            'comments': comments,
            'comment_upvotes': comment_upvotes,
            'post_sentiment': post_sentiment,
            'avg_comment_sentiment': avg_comment_sentiment
    })

        
    json_file_path = '/tmp/reddit_data.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(reddit_data, f, indent=2)

    # Upload to S3
    s3 = boto3.client('s3')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    s3_key = f'reddit_data/reddit_data_{timestamp}.json'
    s3.upload_file(json_file_path, S3_BUCKET_NAME, s3_key)

    return {
        'statusCode': 200,
        'body': f'Uploaded JSON to s3://{S3_BUCKET_NAME}/{s3_key}'
    }

