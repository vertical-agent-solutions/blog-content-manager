import requests
from typing import List, Dict
from django.conf import settings

class WordPressService:
    def __init__(self):
        self.wp_url = settings.WORDPRESS_API_URL
        self.base_api_url = f"{self.wp_url}/wp-json/wp/v2"

    def get_posts(self, per_page: int = 10, page: int = 1) -> List[Dict]:
        """
        Fetch published posts from WordPress
        
        Args:
            per_page (int): Number of posts per page
            page (int): Page number
            
        Returns:
            List[Dict]: List of posts with their data
        """
        try:
            response = requests.get(
                f"{self.base_api_url}/posts",
                params={
                    "per_page": per_page,
                    "page": page,
                    "status": "publish",
                    "_fields": "id,title,excerpt,link,date,content,categories"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching WordPress posts: {e}")
            return []

    def get_post_content(self, post_id: int) -> Dict:
        """
        Fetch full content of a specific post
        
        Args:
            post_id (int): WordPress post ID
            
        Returns:
            Dict: Post data including full content
        """
        try:
            response = requests.get(
                f"{self.base_api_url}/posts/{post_id}",
                params={"_fields": "id,title,content,excerpt,link,date,categories"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching WordPress post content: {e}")
            return {}

    def get_categories(self) -> List[Dict]:
        """
        Fetch all WordPress categories
        
        Returns:
            List[Dict]: List of categories with their data
        """
        try:
            response = requests.get(
                f"{self.base_api_url}/categories",
                params={"per_page": 100, "_fields": "id,name,description"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching WordPress categories: {e}")
            return []

    def get_posts_by_category(self, category_id: int, per_page: int = 10) -> List[Dict]:
        """
        Fetch posts from a specific category
        
        Args:
            category_id (int): WordPress category ID
            per_page (int): Number of posts to fetch
            
        Returns:
            List[Dict]: List of posts in the category
        """
        try:
            response = requests.get(
                f"{self.base_api_url}/posts",
                params={
                    "categories": category_id,
                    "per_page": per_page,
                    "status": "publish",
                    "_fields": "id,title,content,excerpt,link,date"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching posts by category: {e}")
            return [] 