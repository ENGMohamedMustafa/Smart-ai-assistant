from .settings import Settings

class DevelopmentSettings(Settings):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
    # Use smaller models for development
    WHISPER_MODEL = "whisper-1"
    GPT_MODEL = "gpt-3.5-turbo"
    DALLE_MODEL = "dall-e-2"
    
    # Smaller chunks for testing
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100