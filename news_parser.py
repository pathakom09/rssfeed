import feedparser
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib



# Database connection
#engine = create_engine('mysql+pymysql://root:Ola@1000@localhost/news_db')
engine = create_engine('mysql+pymysql://root:Ola%401000@localhost/news_db')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the News Article model
class NewsArticle(Base):
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    publication_date = Column(DateTime)
    source_url = Column(String(255))
    category = Column(String(50))

# Create the table if not exists
Base.metadata.create_all(engine)

# RSS feeds list
rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def fetch_and_store_articles():
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Check if the article already exists in the DB by checking the hash of the title
            article_hash = hashlib.sha256(entry.title.encode('utf-8')).hexdigest()
            if session.query(NewsArticle).filter_by(title=entry.title).first():
                continue  # Skip duplicates
            
            # Safely retrieve publication date
            if 'published_parsed' in entry:
                pub_date = datetime(*entry.published_parsed[:6])
            elif 'updated_parsed' in entry:  # Fallback to updated date if available
                pub_date = datetime(*entry.updated_parsed[:6])
            else:
                pub_date = datetime.now()  # Use current date as fallback

            article = NewsArticle(
                title=entry.title,
                content=entry.get('summary', 'No content'),
                publication_date=pub_date,
                source_url=entry.link,
                category=None  # To be filled after classification
            )
            session.add(article)

        session.commit()  # Commit after processing all entries for a feed

if __name__ == '__main__':
    fetch_and_store_articles()
