import os
import json
from typing import Dict, List
import google.generativeai as genai
from django.conf import settings

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

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
        prompt = f"""Generate {count} blog topic ideas for the category '{category_name}'.
        For each topic, provide:
        1. An engaging title
        2. A brief description (2-3 sentences)
        
        Format the response as a JSON array with 'title' and 'description' fields."""
        
        response = self.model.generate_content(prompt)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return []

    def generate_topics_from_posts(self, posts: List[Dict], count: int = 3) -> List[Dict]:
        """
        Generate new topic ideas based on existing WordPress posts
        
        Args:
            posts (List[Dict]): List of WordPress posts
            count (int): Number of topics to generate
            
        Returns:
            List[Dict]: List of generated topics
        """
        # Create a summary of existing posts
        post_summaries = "\n".join([
            f"- {post['title']['rendered']}: {post['excerpt']['rendered']}"
            for post in posts[:5]  # Use up to 5 posts for context
        ])
        
        prompt = f"""Based on these existing blog posts:

{post_summaries}

Generate {count} new blog topic ideas that would complement the existing content.
Each topic must have:
1. A clear, engaging title
2. A 2-3 sentence description explaining the topic

Return the response in this exact JSON format:
[
    {{
        "title": "Topic Title",
        "description": "Topic description here"
    }},
    ...
]

Make sure:
1. The topics are related but not duplicates of existing content
2. Fill gaps in the current content
3. Provide fresh perspectives or deeper dives
4. The response is valid JSON with exactly {count} topics
5. Each topic has both title and description fields"""
        
        response = self.model.generate_content(prompt)
        try:
            topics = self._parse_topic_ideas(response.text)
            if not topics:  # If parsing failed, try direct JSON parsing
                topics = json.loads(response.text)
            return topics
        except json.JSONDecodeError:
            print(f"Error parsing response: {response.text}")
            return []

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