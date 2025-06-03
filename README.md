# StoryLens - Multi-modal Photo Story Generator

StoryLens is an AI-powered application that generates creative stories and poems from your photos, with optional audio narration.

## Features

- Upload photos and get AI-generated stories or poems
- Powered by OpenAI's GPT-4 Vision API for image understanding and story generation
- Audio narration using OpenAI's Text-to-Speech API
- Beautiful, user-friendly interface

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   **IMPORTANT:** The `.env` file contains sensitive information and should never be committed to version control. The repository's `.gitignore` is configured to ignore this file.

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Technologies Used

- Flask (Backend)
- OpenAI GPT-4 Vision API (Image Understanding & Story Generation)
- OpenAI TTS API (Text-to-Speech)
- HTML/CSS/JavaScript (Frontend)

## Note

This application requires an OpenAI API key to function properly. You will need to provide your own API key in the `.env` file. The application uses GPT-4 Vision for image analysis and story generation, and the TTS-1 model for audio narration.

This application requires significant computational resources for running the AI models. Consider using a machine with a GPU for optimal performance.
