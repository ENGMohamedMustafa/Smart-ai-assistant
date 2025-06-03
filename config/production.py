from .settings import Settings

class ProductionSettings(Settings):
    DEBUG = False
    LOG_LEVEL = "INFO"
    
    # Use premium models for production
    WHISPER_MODEL = "whisper-1"
    GPT_MODEL = "gpt-4"
    DALLE_MODEL = "dall-e-3"
    
    # Optimized chunks for production
    CHUNK_SIZE = 1500
    CHUNK_OVERLAP = 300
    
    # Production security settings
    ALLOWED_HOSTS = ["your-domain.com", "www.your-domain.com"]
    SSL_REQUIRED = True