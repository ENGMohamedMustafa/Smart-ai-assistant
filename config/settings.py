# Configuration settings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI API
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Model configurations
    WHISPER_MODEL = "whisper-1"
    GPT_MODEL = "gpt-4"
    DALLE_MODEL = "dall-e-3"
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assets"
    DOCUMENTS_DIR = ASSETS_DIR / "documents"
    IMAGES_DIR = ASSETS_DIR / "generated_images"
    TEMP_AUDIO_DIR = ASSETS_DIR / "temp_audio"
    
    # Vector database
    VECTOR_DB_PATH = BASE_DIR / "vector_db"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'Arabic': 'ar',
        'English': 'en',
        'French': 'fr',
        'Spanish': 'es',
        'German': 'de'
    }
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        for dir_path in [cls.DOCUMENTS_DIR, cls.IMAGES_DIR, cls.TEMP_AUDIO_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)