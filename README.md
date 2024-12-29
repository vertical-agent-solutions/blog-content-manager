# Content Management with AI

A Django application that uses Google's Gemini AI to generate blog content. This application allows you to manage topics, generate articles, and organize content by categories.

## Features

- Topic Management
  - Create topics manually
  - Generate AI-powered topic suggestions
  - Review and select topics before saving

- Content Generation
  - Generate full articles from topics
  - Markdown formatting support

- Database Management
  - Reset database
  - Seed with sample data
  - Track content status (draft, in progress, published)

## Prerequisites

- Python 3.x
- A Google Cloud project with the Gemini API enabled
- Gemini API key

## Setup

1. Clone this repository

2. Create a `.env` file in the root directory:
   ```
   DJANGO_SECRET_KEY=your-django-secret-key
   GEMINI_API_KEY=your-gemini-api-key
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

2. Managing Topics
   - View all topics in the Topics section
   - Create topics manually using the form
   - Generate topic ideas using AI:
     - Select a category
     - Choose number of topics to generate
     - Review generated topics
     - Select which topics to save

3. Generating Articles
   - Select a draft topic
   - Click "Generate Article"
   - Article is saved with markdown formatting

## Project Structure

```
content-agent/
├── content_manager/          # Django project settings
├── core/                    # Main application
│   ├── services/           # AI services
│   │   └── ai_service.py   # Gemini AI integration
│   ├── templates/          # HTML templates
│   ├── models.py           # Database models
│   └── views.py            # View logic
├── templates/              # Global templates
├── manage.py
├── requirements.txt
└── topics.json             # Seed data
```

## Development

- Built with Django 5.0
- Uses Bootstrap 5 for UI
- SQLite database for local development
- Google's Gemini AI for content generation
- Markdown support for article formatting

## License

This project is licensed under the MIT License

