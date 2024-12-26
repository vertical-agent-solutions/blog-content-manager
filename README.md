# Content Agent

A simple Python application that uses Google's Gemini AI model to generate content.

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
   ```
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On Unix or MacOS
   source env/bin/activate
   ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
