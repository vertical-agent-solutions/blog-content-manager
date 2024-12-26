# main.py

# Standard library imports
import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List

# Third party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class ArticleDatabase:
    def __init__(self, db_name: str = "articles.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                seo_score FLOAT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_article(self, topic: str, content: str, seo_score: float = 0.0) -> int:
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO articles (topic, content, seo_score, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
            (topic, content, seo_score, now, now)
        )
        self.conn.commit()
        return cursor.lastrowid

class ContentAgent:
    def __init__(self, model_name: str = "gemini-pro"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
    
    def generate_article(self, topic: str) -> str:
        prompt = f"""
        Generate a comprehensive article about {topic}.
        The article should be well-structured and informative.
        Format the output in markdown.
        Include:
        - An engaging introduction
        - Multiple subheadings
        - A conclusion
        """
        response = self.model.generate_content(prompt)
        return response.text

class ReviewAgent:
    def __init__(self, model_name: str = "gemini-pro"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
    
    def review_article(self, content: str) -> Dict:
        prompt = f"""
        Review the following article and provide feedback:
        {content}
        
        Provide feedback in JSON format with the following structure:
        {{
            "quality_score": float (1-10),
            "suggestions": list of improvement points,
            "grammar_issues": list of issues
        }}
        """
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

class SEOAgent:
    def __init__(self, model_name: str = "gemini-pro"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
    
    def optimize_article(self, topic: str, content: str) -> Dict:
        prompt = f"""
        Analyze and optimize the following article for SEO:
        Topic: {topic}
        Content: {content}
        
        Provide feedback in JSON format with the following structure:
        {{
            "seo_score": float (1-10),
            "suggested_keywords": list of keywords,
            "optimized_content": string (markdown formatted content),
            "meta_description": string
        }}
        """
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

def main():
    # Initialize database and agents
    db = ArticleDatabase()
    content_agent = ContentAgent()
    review_agent = ReviewAgent()
    seo_agent = SEOAgent()
    
    # Example topic
    topic = "Vertical AI Agents"
    
    # Generate initial content
    print(f"Generating article about: {topic}")
    initial_content = content_agent.generate_article(topic)
    
    # Review the content
    print("Reviewing article...")
    review_feedback = review_agent.review_article(initial_content)
    
    # Optimize for SEO
    print("Optimizing for SEO...")
    seo_results = seo_agent.optimize_article(topic, initial_content)
    
    # Save the optimized article
    article_id = db.save_article(
        topic=topic,
        content=seo_results["optimized_content"],
        seo_score=seo_results["seo_score"]
    )
    
    print(f"Article saved with ID: {article_id}")
    print(f"SEO Score: {seo_results['seo_score']}")
    print("\nGenerated Article:")
    print("=" * 80)
    print(seo_results["optimized_content"])

if __name__ == "__main__":
    main()

