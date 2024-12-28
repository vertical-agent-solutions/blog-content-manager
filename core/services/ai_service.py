import os
import json
from typing import Dict, List
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
        - Only return article content
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def generate_topic_ideas(self, category_name: str, count: int = 3) -> List[Dict]:
        """Generate topic ideas for a given category."""
        prompt = f"""
        Generate {count} blog topic ideas for the category: {category_name}
        
        For each topic provide:
        - Title
        - Brief description (2-3 sentences)
        
        Return the response in this exact JSON format:
        [
            {{
                "title": "Topic Title",
                "description": "Brief description"
            }},
            {{
                "title": "Another Topic",
                "description": "Another description"
            }}
        ]

        Ensure the response is valid JSON and includes exactly {count} topics.
        """
        
        response = self.model.generate_content(prompt)
        return self._parse_topic_ideas(response.text)

    def _parse_topic_ideas(self, text: str) -> List[Dict]:
        """Parse the generated topic ideas from JSON format."""
        try:
            # Clean the text to ensure it only contains the JSON part
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            # Parse the JSON
            topics = json.loads(text)
            
            # Validate the structure
            if not isinstance(topics, list):
                raise ValueError("Response is not a list of topics")
            
            for topic in topics:
                if not isinstance(topic, dict):
                    raise ValueError("Topic is not a dictionary")
                if 'title' not in topic or 'description' not in topic:
                    raise ValueError("Topic missing required fields")
            
            return topics
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw text: {text}")
            return []
        except Exception as e:
            print(f"Error parsing topic ideas: {e}")
            return [] 