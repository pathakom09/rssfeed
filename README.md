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


```
## Setup

1. **Install Redis**: Make sure you have Redis installed and running on your local machine. You can download and install it from [Redis.io](https://redis.io/download).

2. **Database Setup**:
   - Set up a MySQL database and update the connection string in the code.
   - The default connection string used in the code is:
     ```python
     engine = create_engine('mysql+pymysql://username:password@localhost/news_db')
     ```
   - Replace `username` and `password` with your MySQL credentials.
   - Run the following code to create the necessary tables in your MySQL database:
     ```python
     from sqlalchemy import create_engine
     from sqlalchemy.ext.declarative import declarative_base
     from sqlalchemy.orm import sessionmaker
     from sqlalchemy import Column, Integer, String, Text, DateTime

     # Database connection
     engine = create_engine('mysql+pymysql://username:password@localhost/news_db')

     Base = declarative_base()

     # Define the News Article model
     class NewsArticle(Base):
         __tablename__ = 'news_articles'
         
         id = Column(Integer, primary_key=True)
         title = Column(String(255))
         content = Column(Text)
         publication_date = Column(DateTime)
         source_url = Column(String(255))
         category = Column(String(50))

     # Create the table if it doesn't exist
     if __name__ == '__main__':
         Base.metadata.create_all(engine)
         print("Database setup complete. Table 'news_articles' is ready.")
     ```

3. **Run the Project**:
   - Start the Redis server.
   - Run the Celery worker in a terminal:
     ```bash
     celery -A tasks worker --loglevel=info
     ```
   - Execute the script to fetch and store articles:
     ```bash
     python your_script_name.py
     ```

4. **Process Articles**:
   - The articles will be classified in the background by Celery. The `process_articles` function will fetch articles that need classification and enqueue the classification tasks.
