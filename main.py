# main.py

# Standard library imports
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

class DatabaseManager:
    def __init__(self, db_name: str = "blog.db"):
        self.db_path = Path(db_name)
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.setup_database()
    
    def setup_database(self):
        """Initialize database with schema."""
        with open('schema.sql', 'r') as f:
            self.conn.executescript(f.read())
            self.conn.commit()
    
    def seed_categories(self) -> None:
        """Seed initial categories."""
        categories = [
            ("Artificial Intelligence", "artificial-intelligence", "Topics related to AI technology and applications"),
            ("Technology Trends", "technology-trends", "Current and future technology trends"),
            ("Industry Solutions", "industry-solutions", "AI applications in specific industries")
        ]
        
        cursor = self.conn.cursor()
        cursor.executemany(
            """INSERT OR IGNORE INTO categories (name, slug, description)
               VALUES (?, ?, ?)""",
            categories
        )
        self.conn.commit()
    
    def seed_topic_ideas(self, topics: List[Dict]) -> None:
        """Seed initial topic ideas."""
        cursor = self.conn.cursor()
        for topic in topics:
            cursor.execute(
                """INSERT OR IGNORE INTO topic_ideas 
                   (title, slug, description, category_id, target_word_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    topic['title'],
                    slugify(topic['title']),
                    topic['description'],
                    topic['category_id'],
                    topic.get('target_word_count', 1500)
                )
            )
        self.conn.commit()

class ContentGenerator:
    def __init__(self, model_name: str = "gemini-pro"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
        self.db = DatabaseManager()
    
    def generate_article(self, topic_id: int) -> Dict:
        """Generate article content for a given topic."""
        cursor = self.db.conn.cursor()
        topic = cursor.execute(
            """SELECT t.*, c.name as category_name 
               FROM topic_ideas t 
               JOIN categories c ON t.category_id = c.id 
               WHERE t.id = ?""",
            (topic_id,)
        ).fetchone()
        
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
    def __init__(self, model_name: str = "gemini-pro"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
    
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

def seed_initial_topics():
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
    
    db = DatabaseManager()
    db.seed_categories()
    db.seed_topic_ideas(topics)

def main():
    # Initialize database and seed data
    print("Setting up database...")
    seed_initial_topics()
    
    # Initialize content generator
    generator = ContentGenerator()
    seo_optimizer = SEOOptimizer()
    
    # Example: Generate article for first topic
    cursor = generator.db.conn.cursor()
    topic = cursor.execute(
        "SELECT id FROM topic_ideas WHERE status = 'draft' LIMIT 1"
    ).fetchone()
    
    if topic:
        print(f"\nGenerating article for topic ID: {topic['id']}")
        article = generator.generate_article(topic['id'])
        
        print("\nOptimizing content for SEO...")
        seo_results = seo_optimizer.optimize_content(article['content'], article['title'])
        
        # Save article
        cursor.execute("""
            INSERT INTO articles (
                topic_id, title, slug, content, seo_score,
                meta_description, keywords, seo_feedback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            topic['id'],
            article['title'],
            article['slug'],
            article['content'],
            seo_results['seo_score'],
            seo_results['meta_description'],
            json.dumps(seo_results['keywords']),
            seo_results['seo_feedback']
        ))
        
        # Update topic status
        cursor.execute(
            "UPDATE topic_ideas SET status = 'published' WHERE id = ?",
            (topic['id'],)
        )
        
        generator.db.conn.commit()
        
        print(f"\nArticle generated and saved!")
        print(f"SEO Score: {seo_results['seo_score']}")
        print(f"Keywords: {', '.join(seo_results['keywords'])}")

if __name__ == "__main__":
    main()

