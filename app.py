import os
import io
import time
import base64
import logging
import json
import requests
from flask import Flask, render_template, request, jsonify
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai_api_key = os.getenv('OPENAI_API_KEY')

# Validate the API key
if not openai_api_key or openai_api_key == 'your_openai_api_key_here':
    logger.warning("OpenAI API key not set or invalid. Please add your API key to the .env file.")
    valid_key = False
else:
    # Use the API key exactly as provided without any modifications
    logger.info(f"API key loaded. Length: {len(openai_api_key)}")
    valid_key = True

# No need to set openai.api_key as we're using direct HTTP requests

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AUDIO_FOLDER'] = 'static/uploads'  # Using the same folder for audio files

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    """Generate a story from an uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        # Read and process the image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Save the image
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        image.save(img_path)
        
        # Generate story
        story = generate_story_from_image(image)
        
        # Encode image to base64 for display
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'story': story,
            'image': img_str,
            'image_path': img_path
        })
    
    except Exception as e:
        logger.error(f"Error generating story: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    """Generate audio narration for a story"""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        text = data['text']
        audio_path = generate_audio_from_text(text)
        
        return jsonify({
            'audio_path': audio_path
        })
    
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return jsonify({'error': str(e)}), 500

def generate_story_from_image(image):
    """Generate a story from an image using OpenAI's GPT-4 Vision API via direct HTTP request"""
    
    try:
        # Check if API key is valid
        if not valid_key:
            logger.warning("OpenAI API key not set. Using fallback story generation.")
            return "Please set your OpenAI API key in the .env file to generate unique stories from your images."
        
        # Save image to a temporary buffer
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        
        # Encode the image as base64
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Log the API key format for debugging
        logger.info(f"Using API key starting with: {openai_api_key[:15]}...")
        
        # Create the API request with direct HTTP
        try:
            # Set up the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            }
            
            # Prepare the request payload
            payload = {
                "model": "gpt-4o",  # Using the latest model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a creative writer that generates short stories or poems based on images. Your stories should be evocative, thoughtful, and capture the essence of the image. Occasionally write poems instead of prose. Keep responses to 150-200 words maximum."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Generate a creative short story or poem inspired by this image:"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            # Make the API request
            logger.info("Making direct HTTP request to GPT-4 Vision API...")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info("GPT-4 Vision API request successful!")
                result = response.json()
                story = result['choices'][0]['message']['content'].strip()
                return story
            else:
                logger.error(f"API request failed with status code {response.status_code}: {response.text}")
                return f"Error connecting to OpenAI API: Status code {response.status_code}. {response.text}"
                
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return f"Error connecting to Hugging Face API: {str(e)}. Please check your internet connection."
        
    except Exception as e:
        logger.error(f"Error in story generation: {e}")
        return f"Sorry, I couldn't generate a story for this image. Error: {str(e)}. Please try again."

def generate_audio_from_text(text):
    """Generate audio narration using OpenAI's Text-to-Speech API via direct HTTP request"""
    try:
        # Check if API key is valid
        if not valid_key:
            logger.warning("OpenAI API key not set. Using fallback audio generation.")
            # Create a placeholder file
            audio_filename = f"audio_{int(time.time())}.mp3"
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            with open(audio_path, 'wb') as f:
                f.write(b'\x00')
            return f"/static/uploads/{audio_filename}"
        
        # Create a unique filename for the audio
        audio_filename = f"audio_{int(time.time())}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        
        try:
            # Set up the API request
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the request payload
            payload = {
                "model": "tts-1",
                "voice": "nova",  # Options: alloy, echo, fable, onyx, nova, shimmer
                "input": text
            }
            
            # Make the API request
            logger.info("Making direct HTTP request to TTS API...")
            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers=headers,
                json=payload,
                stream=True
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info("TTS API request successful!")
                
                # Save the audio file
                with open(audio_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"Audio saved to {audio_path}")
                return f"/static/uploads/{audio_filename}"
            else:
                logger.error(f"API request failed with status code {response.status_code}: {response.text}")
                raise Exception(f"Failed to generate audio: Status code {response.status_code}. {response.text}")
        
        except Exception as e:
            logger.error(f"Error in TTS API call: {e}")
            raise
    
    except Exception as e:
        logger.error(f"Error in audio generation: {e}")
        # Fallback to a placeholder audio file
        audio_filename = f"audio_{int(time.time())}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        with open(audio_path, 'wb') as f:
            f.write(b'\x00')
        return f"/static/uploads/{audio_filename}"

if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True)
