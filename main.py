# main.py

# Standard library imports
import os
import json
from typing import Dict, List
import re

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports
from database import DatabaseManager
from content_generator import ContentGenerator, SEOOptimizer

# Load environment variables
load_dotenv()

# Configure AI model once
THINKING_MODEL = "gemini-2.0-flash-thinking-exp-1219"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(THINKING_MODEL)

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def load_seed_data() -> Dict:
    """Load seed data from topics.json."""
    with open('topics.json', 'r') as f:
        return json.load(f)

def seed_initial_topics(db: DatabaseManager):
    """Seed the database with initial topics."""
    seed_data = load_seed_data()
    
    # Seed categories first
    for category in seed_data['categories']:
        db.seed_category(category)
    
    # Then seed topics
    db.seed_topic_ideas(seed_data['topics'])

def main():
    # Initialize database and seed data
    print("Setting up database...")
    db = DatabaseManager()
    seed_initial_topics(db)
    
    # Initialize content generator and SEO optimizer
    generator = ContentGenerator(db, model)
    seo_optimizer = SEOOptimizer(model)
    
    # Get draft topic
    topic = db.get_draft_topic()
    
    if topic:
        print(f"\nGenerating article for topic ID: {topic['id']}")
        article = generator.generate_article(topic['id'])
        
        print("\nOptimizing content for SEO...")
        seo_results = seo_optimizer.optimize_content(article['content'], article['title'])
        
        # Save article and update topic status
        db.save_article(article, seo_results)
        
        print(f"\nArticle generated and saved!")
        print(f"SEO Score: {seo_results['seo_score']}")
        print(f"Keywords: {', '.join(seo_results['keywords'])}")

if __name__ == "__main__":
    main()

