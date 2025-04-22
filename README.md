# Reddit-Solana

# 📊 Reddit Sentiment Dashboard for r/Solana

A  AWS pipeline to analyze and visualize sentiment in discussions from the [r/Solana](https://www.reddit.com/r/solana/) subreddit.

Built using:
- 🐍 Python + [PRAW](https://praw.readthedocs.io/) for Reddit scraping
- 🧠 VADER Sentiment Analysis
- ☁️ AWS Lambda + S3 for data storage
- 🔍 Amazon QuickSight for dashboarding

---

## 📌 Project Overview

This project tracks public sentiment and engagement trends across Reddit posts and comments from the Solana community. The pipeline fetches the latest posts, analyzes sentiment, and sends the structured data to S3 for visualization in QuickSight.



---

## 🔧 Pipeline Components

| Step | Description |
|------|-------------|
| **Data Collection** | Reddit data fetched via `praw`, 10 latest posts + comments |
| **Sentiment Analysis** | VADER used to compute post + comment sentiment |
| **Storage** | JSON Lines format written to S3 bucket via AWS Lambda |
| **Visualization** | Amazon QuickSight dashboard using manifest-based data import |

---

## 🧪 Key Metrics & Visuals

- **📅 Sentiment Over Time** – line graph of post sentiment
- **🔥 Top Upvoted Posts** – bar chart with titles and upvotes
- **🧠 Comment Sentiment Distribution** – histogram
- **⚡ Activity Heatmap** – posts by day/hour
- **💬 Author Leaderboard** – most active users by posts & sentiment

---

## 📂 Sample Data

```json
{
  "title": "Would you say most people on this sub aren't crypto devs?",
  "author": "Anomalous-X",
  "url": "https://www.reddit.com/r/solana/comments/...",
  "created_utc": "2025-04-21 23:30:41",
  "upvotes": 2,
  "comments": ["Most people...", "Bro, I have been using Linux..."],
  "comment_upvotes": 16,
  "post_sentiment": 0.0,
  "avg_comment_sentiment": 0.3123
}
