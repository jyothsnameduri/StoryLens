# StoryLens

Transform your images into compelling narratives with this AI-powered creative storytelling application.

## What It Does

- Converts your uploaded images into unique stories and poetry
- Uses advanced AI to analyze visual content and craft engaging narratives
- Delivers audio versions of generated stories through text-to-speech technology
- Features an intuitive and responsive user interface

## Getting Started

1. Set up dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your API credentials:
   ```
   # Create a file named .env with the following content
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   **SECURITY NOTE:** Never commit your `.env` file to version control. This file has been added to `.gitignore` to prevent accidental exposure of your API key.

3. Launch the application:
   ```
   python app.py
   ```

4. Access the web interface at `http://localhost:5000`

## Technology Stack

- **Backend Framework:** Flask
- **Image Analysis & Text Generation:** OpenAI GPT-4 Vision API
- **Voice Synthesis:** OpenAI TTS API
- **Frontend:** HTML, CSS, and JavaScript

## Important Information

This project requires a valid OpenAI API key to function. You must supply your own key in the `.env` file as described above.

The application leverages computationally intensive models - GPT-4 Vision for analyzing images and generating narratives, and TTS-1 for creating spoken audio. For best performance, running on hardware with GPU acceleration is recommended.
