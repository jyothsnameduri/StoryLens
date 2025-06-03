document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadArea = document.getElementById('upload-area');
    const fileUpload = document.getElementById('file-upload');
    const resultContainer = document.getElementById('result-container');
    const loadingContainer = document.getElementById('loading-container');
    const uploadedImage = document.getElementById('uploaded-image');
    const storyText = document.getElementById('story-text');
    const newStoryBtn = document.getElementById('new-story-btn');
    const generateAudioBtn = document.getElementById('generate-audio-btn');
    const audioPlayer = document.getElementById('audio-player');
    const audioElement = document.getElementById('audio-element');
    const downloadAudioBtn = document.getElementById('download-audio-btn');
    const loadingText = document.getElementById('loading-text');

    // Event Listeners
    uploadArea.addEventListener('click', () => fileUpload.click());
    fileUpload.addEventListener('change', handleFileUpload);
    newStoryBtn.addEventListener('click', resetApp);
    generateAudioBtn.addEventListener('click', generateAudio);
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.backgroundColor = 'var(--light-gray)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--medium-gray)';
        uploadArea.style.backgroundColor = 'white';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--medium-gray)';
        uploadArea.style.backgroundColor = 'white';
        
        if (e.dataTransfer.files.length) {
            fileUpload.files = e.dataTransfer.files;
            handleFileUpload();
        }
    });

    // Functions
    function handleFileUpload() {
        const file = fileUpload.files[0];
        
        if (!file) return;
        
        // Check if file is an image
        if (!file.type.match('image.*')) {
            alert('Please upload an image file');
            return;
        }
        
        // Check file size (max 16MB)
        if (file.size > 16 * 1024 * 1024) {
            alert('File size exceeds 16MB limit');
            return;
        }
        
        // Show loading screen
        loadingContainer.classList.remove('hidden');
        loadingText.textContent = 'Generating your story...';
        
        // Create FormData
        const formData = new FormData();
        formData.append('image', file);
        
        // Send image to server
        fetch('/generate_story', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display results
            uploadedImage.src = `data:image/jpeg;base64,${data.image}`;
            storyText.textContent = data.story;
            
            // Show result container
            resultContainer.classList.remove('hidden');
            loadingContainer.classList.add('hidden');
            
            // Reset audio player
            audioPlayer.classList.add('hidden');
            audioElement.src = '';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating story. Please try again.');
            loadingContainer.classList.add('hidden');
        });
    }

    function generateAudio() {
        // Show loading screen
        loadingContainer.classList.remove('hidden');
        loadingText.textContent = 'Generating audio narration...';
        
        // Get story text
        const text = storyText.textContent;
        
        // Send text to server
        fetch('/generate_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Set audio source
            audioElement.src = data.audio_path;
            
            // Set download link
            downloadAudioBtn.href = data.audio_path;
            
            // Show audio player
            audioPlayer.classList.remove('hidden');
            loadingContainer.classList.add('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating audio. Please try again.');
            loadingContainer.classList.add('hidden');
        });
    }

    function resetApp() {
        // Hide result container
        resultContainer.classList.add('hidden');
        
        // Reset file input
        fileUpload.value = '';
        
        // Reset audio player
        audioPlayer.classList.add('hidden');
        audioElement.src = '';
    }
});
