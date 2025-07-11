# Image generation service
import openai
import requests
from datetime import datetime
import json
from pathlib import Path
from config.settings import Settings

class DalleService:
    def __init__(self):
        openai.api_key = Settings.OPENAI_API_KEY
        self.model = Settings.DALLE_MODEL
        self.generated_images = []
        self._load_image_history()
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """
        Generate image using DALL-E
        
        Args:
            prompt: Image description
            size: Image size
            quality: Image quality
            
        Returns:
            Image URL
        """
        try:
            response = openai.Image.create(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            image_url = response.data[0].url
            
            # Save image data
            image_data = {
                'prompt': prompt,
                'url': image_url,
                'timestamp': datetime.now().isoformat(),
                'size': size,
                'quality': quality
            }
            
            self.generated_images.append(image_data)
            self._save_image_history()
            
            return image_url
            
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
    
    def get_generated_images(self) -> list:
        """Get list of generated images"""
        return self.generated_images
    
    def _load_image_history(self):
        """Load image generation history"""
        history_file = Settings.IMAGES_DIR / "history.json"
        try:
            if history_file.exists():
                with open(history_file, 'r') as f:
                    self.generated_images = json.load(f)
        except Exception as e:
            print(f"Image history load error: {e}")
            self.generated_images = []
    
    def _save_image_history(self):
        """Save image generation history"""
        history_file = Settings.IMAGES_DIR / "history.json"
        try:
            Settings.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            with open(history_file, 'w') as f:
                json.dump(self.generated_images, f, indent=2)
        except Exception as e:
            print(f"Image history save error: {e}")