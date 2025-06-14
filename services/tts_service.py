# Text-to-speech service
from gtts import gTTS
import tempfile
import os
from pathlib import Path
from config.settings import Settings

class TTSService:
    def __init__(self):
        self.temp_dir = Settings.TEMP_AUDIO_DIR
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_speech(self, text: str, language: str = "English") -> str:
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            language: Target language
            
        Returns:
            Path to generated audio file
        """
        try:
            # Map language names to gTTS language codes
            lang_map = {
                'Arabic': 'ar',
                'English': 'en',
                'French': 'fr',
                'Spanish': 'es',
                'German': 'de'
            }
            
            lang_code = lang_map.get(language, 'en')
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to temporary file
            temp_file = self.temp_dir / f"tts_{hash(text)}.mp3"
            tts.save(str(temp_file))
            
            return str(temp_file)
            
        except Exception as e:
            print(f"TTS generation error: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file in self.temp_dir.glob("*.mp3"):
                if file.exists():
                    os.unlink(file)
        except Exception as e:
            print(f"Cleanup error: {e}")