🧠 Multi-Modal AI Assistant

A comprehensive AI-powered assistant that combines speech-to-text, translation, RAG (Retrieval-Augmented Generation), image generation, and text-to-speech capabilities in a single, user-friendly interface.

## ✨ Features

- 🎤 **Speech-to-Text**: Convert audio to text using OpenAI Whisper
- 🌍 **Multi-Language Translation**: Real-time translation support
- 📚 **RAG Integration**: Context-aware responses using your documents
- 🎨 **Image Generation**: Create images using DALL-E 3
- 🔊 **Text-to-Speech**: Convert responses to audio
- 💬 **Interactive Chat**: Streamlit-based user interface
- 📊 **Analytics Dashboard**: Track usage and performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multimodal-ai-assistant.git
cd multimodal-ai-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the application:
```bash
streamlit run app.py
```

## 🏗️ Project Structure

```
multimodal-ai-assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .env.example             # Environment variables template
├── config/
│   └── settings.py          # Configuration settings
├── services/                # AI service implementations
│   ├── whisper_service.py   # Speech-to-text
│   ├── translation_service.py # Translation
│   ├── rag_service.py       # RAG implementation
│   ├── dalle_service.py     # Image generation
│   └── tts_service.py       # Text-to-speech
├── utils/                   # Utility functions
│   ├── file_processor.py    # Document processing
│   ├── vector_db.py        # Vector database operations
│   └── session_manager.py   # Session management
└── assets/                 # Static assets and storage
    ├── documents/          # Knowledge base files
    ├── generated_images/   # Generated images
    └── temp_audio/        # Temporary audio files
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `WHISPER_MODEL`: Whisper model to use (default: whisper-1)
- `GPT_MODEL`: GPT model for RAG responses (default: gpt-4)
- `DALLE_MODEL`: DALL-E model for image generation (default: dall-e-3)

### Supported Languages
- Arabic (العربية)
- English
- French (Français)
- Spanish (Español)
- German (Deutsch)

## 📖 Usage Guide

### 1. Chat Interface
- **Text Input**: Type messages directly
- **Audio Upload**: Upload audio files for transcription
- **Live Recording**: Record audio directly (requires WebRTC setup)

### 2. Knowledge Base Management
- Upload PDF, TXT, or DOCX files
- Documents are automatically processed and indexed
- RAG system uses your documents to provide contextual responses

### 3. Image Generation
- Include keywords like "generate image", "create picture", or "draw"
- Images are generated using DALL-E 3
- All generated images are saved in the gallery

### 4. Multi-Language Support
- Select target language from sidebar
- Automatic translation of responses
- Text-to-speech in multiple languages

## 🔌 API Integration

### OpenAI Services Used
- **Whisper API**: Speech-to-text transcription
- **GPT-4 API**: Text generation and RAG responses
- **DALL-E 3 API**: Image generation
- **Embeddings API**: Document vectorization

### External Services
- **Google Translate**: Multi-language translation
- **gTTS**: Text-to-speech conversion
- **FAISS**: Vector similarity search

## 🛠️ Development

### Adding New Features

1. **New AI Service**: Create a new service in `services/` directory
2. **UI Components**: Add new tabs or sections in `app.py`
3. **Configuration**: Update `config/settings.py` for new parameters

### Custom Styling
- Modify `static/styles.css` for UI customization
- Use Streamlit's theming system for colors and fonts

### Database Integration
- Vector database using FAISS for document embeddings
- Session data stored in JSON files
- Analytics tracked automatically

## 📊 Analytics & Monitoring

The application tracks:
- Total messages processed
- Images generated
- Documents added to knowledge base
- Audio files processed
- Session history and usage patterns

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run app.py --server.port 8501
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

### Cloud Deployment
- **Streamlit Cloud**: Connect GitHub repository
- **Heroku**: Use Procfile with `web: streamlit run app.py`
- **AWS/GCP**: Deploy using container services

## 🔒 Security Considerations

- API keys stored in environment variables
- File uploads validated and sanitized
- Temporary files automatically cleaned up
- No sensitive data stored in logs

## 🧪 Testing

```bash
# Run basic functionality tests
python -m pytest tests/

# Test individual services
python -c "from services.whisper_service import WhisperService; print('Whisper OK')"
python -c "from services.rag_service import RAGService; print('RAG OK')"
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify API key in `.env` file
   - Check API usage limits and billing

2. **Audio Processing Issues**
   - Ensure audio files are in supported formats (WAV, MP3, M4A)
   - Check file size limits

3. **Vector Database Errors**
   - Delete `vector_db/` directory to reset
   - Ensure sufficient disk space for embeddings

4. **Translation Errors**
   - Google Translate may have rate limits
   - Consider using paid translation APIs for production

### Performance Optimization

- Use smaller chunk sizes for faster processing
- Implement caching for frequently accessed data
- Consider using GPU acceleration for large models

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for Whisper, GPT-4, and DALL-E APIs
- Streamlit team for the amazing framework
- LangChain community for RAG implementation
- Google for translation services

## 📞 Support

- Create an issue on GitHub
- Email: mohamedmshaban99.com
- 

## 13. Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p assets/documents assets/generated_images assets/temp_audio

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.address", "0.0.0.0"]
```
