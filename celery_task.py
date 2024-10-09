from celery import Celery
from sqlalchemy.orm import sessionmaker
from news_parser import NewsArticle, engine
import spacy

# Initialize spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Celery setup
celery = Celery('tasks', broker='redis://localhost:6379/0')

# Task queue processor
Session = sessionmaker(bind=engine)
session = Session()

@celery.task
def classify_and_update_article(article_id):
    article = session.query(NewsArticle).get(article_id)
    if not article:
        return

    doc = nlp(article.content)
    
    # Simple keyword-based classification
    if any(word in doc.text.lower() for word in ["terrorism", "protest", "riot", "unrest"]):
        article.category = "Terrorism / protest / political unrest / riot"
    elif any(word in doc.text.lower() for word in ["earthquake", "flood", "disaster", "hurricane"]):
        article.category = "Natural Disasters"
    elif any(word in doc.text.lower() for word in ["inspiring", "positive", "uplifting", "hope"]):
        article.category = "Positive/Uplifting"
    else:
        article.category = "Others"
    
    session.commit()

def process_articles():
    articles = session.query(NewsArticle).filter(NewsArticle.category.is_(None)).all()
    for article in articles:
        classify_and_update_article.delay(article.id)

if __name__ == '__main__':
    process_articles()
