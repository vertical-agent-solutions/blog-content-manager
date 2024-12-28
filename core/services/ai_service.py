import os
from typing import Dict
import google.generativeai as genai
from django.conf import settings

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def generate_article(self, topic: Dict) -> str:
        """Generate article content for a given topic."""
        prompt = f"""
        Write a comprehensive article about this topic: {topic.title}
        Additional context: {topic.description}
        
        Requirements:
        - The article should be around {topic.target_word_count} words long
        - Write in markdown format
        - Include a compelling introduction
        - Use appropriate subheadings
        - Include a conclusion
        - Focus on providing valuable insights
        - Be engaging, simple, and informative
        - Add source references when available
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_topic_ideas(self, category_name: str, count: int = 3) -> list:
        """Generate topic ideas for a given category."""
        prompt = f"""
        Generate {count} blog topic ideas for the category: {category_name}
        
        For each topic provide:
        - Title
        - Brief description (2-3 sentences)
        - Target word count (between 1000-2500)
        
        Return the response in this exact format:
        1. Title: [topic title]
           Description: [description]
           Word Count: [number]
        
        2. Title: [topic title]
           Description: [description]
           Word Count: [number]
        
        (and so on...)
        """
        
        response = self.model.generate_content(prompt)
        return self._parse_topic_ideas(response.text)

    def _parse_topic_ideas(self, text: str) -> list:
        """Parse the generated topic ideas into a structured format."""
        topics = []
        current_topic = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Title:'):
                if current_topic:
                    topics.append(current_topic)
                current_topic = {'title': line[6:].strip()}
            elif line.startswith('Description:'):
                current_topic['description'] = line[12:].strip()
            elif line.startswith('Word Count:'):
                current_topic['target_word_count'] = int(line[11:].strip())
        
        if current_topic:
            topics.append(current_topic)
            
        return topics 