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
        - Write in simple markdown format
        - The article should be near 2500 words long
        - Include a compelling introduction
        - Use appropriate subheadings
        - Include a conclusion
        - Focus on providing clear and valuable insights
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_topic_ideas(self, category_name: str, count: int = 3) -> list:
        """Generate topic ideas for a given category."""
        prompt = """
        Generate {} blog topic ideas for the category: {}
        
        For each topic provide:
        - Title
        - Brief description (2-3 sentences)
        
        Return the response in JSON format:
        [
            {"title": "Topic Title", "description": "Brief description"},
            {"title": "Topic Title", "description": "Brief description"},
            {"title": "Topic Title", "description": "Brief description"}
        ]
        """.format(category_name=category_name, count=count)
        print(prompt)
        
        response = self.model.generate_content(prompt)
        print(response.text)
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
        
        if current_topic:
            topics.append(current_topic)
            
        return topics 