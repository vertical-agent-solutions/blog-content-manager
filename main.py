# main.py

# Standard library imports
import json
import os
from typing import Dict, List
import re

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports
from database import DatabaseManager

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

class ContentGenerator:
    def __init__(self, db: DatabaseManager):
        self.model = model  # Use shared model instance
        self.db = db
    
    def generate_article(self, topic_id: int) -> Dict:
        """Generate article content for a given topic."""
        topic = self.db.get_topic_details(topic_id)
        
        prompt = f"""
        Write a comprehensive article about: {topic['title']}
        Category: {topic['category_name']}
        Target word count: {topic['target_word_count']}
        
        Requirements:
        - Write in markdown format
        - Include a compelling introduction
        - Use appropriate subheadings
        - Include a conclusion
        - Focus on providing valuable insights
        - Be engaging and informative
        
        Additional context: {topic['description']}
        """
        
        response = self.model.generate_content(prompt)
        return {
            'content': response.text,
            'topic_id': topic_id,
            'title': topic['title'],
            'slug': topic['slug']
        }

class SEOOptimizer:
    def __init__(self):
        self.model = model  # Use shared model instance
    
    def optimize_content(self, content: str, title: str) -> Dict:
        """Optimize content for SEO."""
        prompt = f"""
        Analyze this article for SEO optimization:
        Title: {title}
        
        Provide feedback in JSON format:
        {{
            "seo_score": float (1-10),
            "meta_description": "compelling 155-character description",
            "keywords": ["list", "of", "relevant", "keywords"],
            "seo_feedback": "detailed feedback and suggestions"
        }}
        
        Content to analyze: {content}
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

def seed_initial_topics(db: DatabaseManager):
    """Seed the database with initial topics."""
    topics = [
        {
            "title": "What are vertical AI agents, and why do they matter?",
            "description": "Explore the concept of vertical AI agents and their impact on specific industries",
            "category_id": 1,
            "target_word_count": 2000
        },
        {
            "title": "Industries that are ripe for AI disruption",
            "description": "Analysis of industries most likely to be transformed by AI technology",
            "category_id": 3,
            "target_word_count": 2500
        },
        {
            "title": "AI in Healthcare: Personalized Diagnostics for Every Patient",
            "description": "How AI is revolutionizing healthcare through personalized medicine",
            "category_id": 3,
            "target_word_count": 2000
        },
        {
            "title": "Real Estate and AI: Transforming Property Searches and Offers",
            "description": "The impact of AI on real estate industry processes and customer experience",
            "category_id": 3,
            "target_word_count": 1800
        },
        {
            "title": "Vertical AI in Education: From Gamified Tools to Customized Learning Paths",
            "description": "How AI is personalizing education and improving learning outcomes",
            "category_id": 3,
            "target_word_count": 2200
        },
        {
            "title": "The Future of Modular AI: Daisy Chains and Specialized Systems",
            "description": "Exploring the concept of modular AI systems and their potential applications",
            "category_id": 1,
            "target_word_count": 2500
        }
    ]
    
    db.seed_categories()
    db.seed_topic_ideas(topics)

def main():
    # Initialize database and seed data
    print("Setting up database...")
    db = DatabaseManager()
    seed_initial_topics(db)
    
    # Initialize content generator and SEO optimizer
    generator = ContentGenerator(db)
    seo_optimizer = SEOOptimizer()
    
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

