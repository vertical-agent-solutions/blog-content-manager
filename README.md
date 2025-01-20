# Blog Content Management with AI

A Django application that uses Google's Gemini AI to generate and manage blog content, with WordPress integration.

## Features

- Topic Management
  - Create topics manually
  - Generate AI-powered topic suggestions
  - Generate topics based on existing WordPress posts
  - Review and select topics before saving
  - Dynamic category management:
    - Select from existing categories
    - Create new categories on the fly
    - Optional category descriptions
    - Duplicate category prevention

- Content Generation
  - Generate full articles from topics using Gemini
  - Clean, structured HTML output
  - Professional formatting with headings and paragraphs
  - Easy content copying:
    - Copy as plain text
    - Copy as HTML
    - One-click clipboard integration

- WordPress Integration
  - Sync and view WordPress posts
  - Use existing posts for content analysis
  - Generate new topic ideas based on published content
  - Track WordPress post synchronization

- Database Management
  - Reset database
  - Seed with sample data
  - Track content status (draft, in progress, published)

## Prerequisites

- Python 3.x
- A Google Cloud project with the Gemini API enabled
- Gemini API key
- WordPress site with REST API enabled

## Setup

1. Clone this repository

2. Create a `.env` file in the root directory:
   ```
   DJANGO_SECRET_KEY=your-django-secret-key
   GEMINI_API_KEY=your-gemini-api-key
   WORDPRESS_API_URL=https://your-wordpress-site.com
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Run database migrations:
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

The application will be available at http://127.0.0.1:8000/

## Usage

1. Initial Setup
   - Visit the home page
   - Use "Seed Database" to populate initial categories and topics
   - Configure your WordPress site URL in `.env`

2. Managing Topics
   - View all topics in the Topics section
   - Create topics manually:
     - Enter topic title and description
     - Either select an existing category or create a new one
     - New categories can include optional descriptions
   - Generate topic ideas using AI:
     - Select a category
     - Choose number of topics to generate
     - Review generated topics
     - Select which topics to save
   - Generate topics from WordPress posts:
     - Sync your WordPress posts
     - Generate topics based on existing content
     - Review and select relevant topics

3. WordPress Integration
   - View synchronized WordPress posts
   - Manually sync posts when needed
   - Use existing posts as inspiration for new topics
   - Generate complementary content ideas

4. Generating Articles
   - Select a draft topic
   - Click "Generate Article"
   - Review the generated content
   - Copy content as plain text or HTML
   - Articles are formatted with clean HTML structure

## Project Structure

```
blog-content-manager/
├── content_manager/          # Django project settings
├── core/                     # Main application
│   ├── services/            # Service layer
│   │   ├── ai_service.py    # Gemini AI integration
│   │   └── wordpress_service.py  # WordPress API integration
│   ├── models.py            # Database models
│   └── views.py             # View logic
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── core/               # Core app templates
├── manage.py
├── requirements.txt
└── topics.json             # Seed data
```

## Development

- Built with Django 5.0
- Uses Bootstrap 5 for UI
- SQLite database for local development
- Google's Gemini AI for content generation
- WordPress REST API integration
- Clean HTML output for articles

## License

This project is licensed under the MIT License

