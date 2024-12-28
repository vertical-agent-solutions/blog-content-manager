# Content Agent

A Django application that uses Google's Gemini AI model to generate blog content. This application allows you to manage topics, generate articles, and organize content by categories.

## Prerequisites

- Python 3.x
- A Google Cloud project with the Gemini API enabled
- Gemini API key

## Setup

1. Clone this repository

2. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
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

## Features

- Topic Management
  - Create topics manually
  - Generate topic ideas using AI
  - Organize topics by categories

- Content Generation
  - Generate full articles from topics
  - Markdown formatting support
  - Customizable word count targets

- Database Management
  - Reset database
  - Seed with sample data
  - Track content status

## Project Structure

```
content-agent/
├── blog_generator/          # Django project settings
├── core/                    # Main application
│   ├── services/           # AI services
│   ├── templates/          # HTML templates
│   ├── models.py           # Database models
│   └── views.py            # View logic
├── templates/              # Global templates
├── manage.py
├── requirements.txt
└── topics.json             # Seed data
```

## Usage

1. After starting the server, visit the home page
2. Use the "Seed Database" button to populate initial categories and topics
3. Navigate to Topics to:
   - View existing topics
   - Create new topics
   - Generate topic ideas
4. Select a topic and click "Generate Article" to create content
5. View all generated articles in the Articles section

## Development

- Built with Django 5.0
- Uses Bootstrap 5 for UI
- SQLite database for local development
- Google's Gemini AI for content generation

## License

This project is licensed under the MIT License

