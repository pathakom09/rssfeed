# News Article Classification System

This project is a News Article Classification System that fetches articles from various RSS feeds, stores them in a MySQL database, and classifies them into categories using Natural Language Processing (NLP) with spaCy. The classification is handled asynchronously using Celery and Redis as the message broker.

## Features

- Fetches articles from multiple RSS feeds.
- Stores articles in a MySQL database.
- Classifies articles into categories: 
  - Terrorism / protest / political unrest / riot
  - Natural Disasters
  - Positive/Uplifting
  - Others
- Uses Celery for asynchronous processing.
- Utilizes spaCy for NLP tasks.

## Technologies Used

- Python
- Celery
- Redis (for task queue)
- SQLAlchemy (ORM for MySQL)
- spaCy (for NLP)
- Feedparser (for parsing RSS feeds)
- MySQL (for database storage)

## Requirements

Make sure to install the following packages:

```bash
pip install celery redis sqlalchemy spacy feedparser pymysql
python -m spacy download en_core_web_sm



Setup
Install Redis: Make sure you have Redis installed and running on your local machine. You can download and install it from Redis.io.

Database Setup:

Set up a MySQL database and update the connection string in the code.
The default connection string used in the code is
