# main.py

# Standard library imports
import os
import json
from typing import Dict, List
from pathlib import Path

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports
from database import DatabaseManager
from content_generator import ContentGenerator

# Load environment variables
load_dotenv()

# Configure AI model once
THINKING_MODEL = "gemini-2.0-flash-thinking-exp-1219"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(THINKING_MODEL)

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
    # Delete existing database if it exists
    db_path = Path("blog.db")
    if db_path.exists():
        print("Removing existing database...")
        db_path.unlink()
    
    # Initialize database and seed data
    print("Setting up fresh database...")
    db = DatabaseManager()
    seed_initial_topics(db)
    
    # Initialize content generator
    generator = ContentGenerator(db, model)
    
    # Get draft topic
    topic = db.get_draft_topic()
    
    if topic:
        print(f"\nGenerating article for topic ID: {topic['id']}")
        article = generator.generate_article(topic['id'])
        
        # Save article
        db.save_article(article)
        
        print(f"\nArticle generated and saved!")
        print("\nGenerated Article:")
        print("=" * 80)
        print(article['content'])

if __name__ == "__main__":
    main()

