# Standard library imports
from typing import Dict

# Third party imports
import google.generativeai as genai

# Local imports
from database import DatabaseManager

class ContentGenerator:
    def __init__(self, db: DatabaseManager, model: genai.GenerativeModel):
        self.model = model
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
        - Be engaging, simple, and informative
        - Be humorous when appropriate
        
        Additional context: {topic['description']}
        """
        
        response = self.model.generate_content(prompt)
        return {
            'content': response.text,
            'topic_id': topic_id,
            'title': topic['title'],
            'slug': topic['slug']
        } 