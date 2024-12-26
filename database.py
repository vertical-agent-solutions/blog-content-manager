# Standard library imports
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

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
    
    def seed_category(self, category: Dict) -> None:
        """Seed a single category."""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO categories (name, slug, description)
               VALUES (?, ?, ?)""",
            (category['name'], category['slug'], category['description'])
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
    
    def get_draft_topic(self) -> sqlite3.Row:
        """Get the first draft topic."""
        cursor = self.conn.cursor()
        return cursor.execute(
            "SELECT id FROM topic_ideas WHERE status = 'draft' LIMIT 1"
        ).fetchone()
    
    def get_topic_details(self, topic_id: int) -> sqlite3.Row:
        """Get detailed topic information."""
        cursor = self.conn.cursor()
        return cursor.execute(
            """SELECT t.*, c.name as category_name 
               FROM topic_ideas t 
               JOIN categories c ON t.category_id = c.id 
               WHERE t.id = ?""",
            (topic_id,)
        ).fetchone()
    
    def save_article(self, article: Dict) -> None:
        """Save generated article and update topic status."""
        cursor = self.conn.cursor()
        
        # Save article
        cursor.execute("""
            INSERT INTO articles (topic_id, title, slug, content)
            VALUES (?, ?, ?, ?)
        """, (
            article['topic_id'],
            article['title'],
            article['slug'],
            article['content']
        ))
        
        # Update topic status
        cursor.execute(
            "UPDATE topic_ideas SET status = 'published' WHERE id = ?",
            (article['topic_id'],)
        )
        
        self.conn.commit() 