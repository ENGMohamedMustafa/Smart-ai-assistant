# Translation service
from googletrans import Translator
from config.settings import Settings

class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.language_codes = Settings.SUPPORTED_LANGUAGES
    
    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language name
            
        Returns:
            Translated text
        """
        try:
            target_code = self.language_codes.get(target_language, 'en')
            result = self.translator.translate(text, dest=target_code)
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'unknown'
    
    def get_supported_languages(self) -> dict:
        """Get all supported languages"""
        return self.language_codes