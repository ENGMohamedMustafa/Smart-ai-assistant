# Session management
import json
from datetime import datetime
from pathlib import Path
from config.settings import Settings

class SessionManager:
    def __init__(self):
        self.analytics_file = Settings.BASE_DIR / "analytics.json"
        self.analytics = self._load_analytics()
    
    def _load_analytics(self) -> dict:
        """Load analytics data"""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            return self._get_default_analytics()
        except Exception as e:
            print(f"Analytics load error: {e}")
            return self._get_default_analytics()
    
    def _get_default_analytics(self) -> dict:
        """Get default analytics structure"""
        return {
            'total_messages': 0,
            'images_generated': 0,
            'documents_processed': 0,
            'audio_processed': 0,
            'sessions': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def update_analytics(self, event_type: str, data: dict = None):
        """Update analytics with new event"""
        try:
            if event_type == 'message':
                self.analytics['total_messages'] += 1
            elif event_type == 'image_generated':
                self.analytics['images_generated'] += 1
            elif event_type == 'document_processed':
                self.analytics['documents_processed'] += 1
            elif event_type == 'audio_processed':
                self.analytics['audio_processed'] += 1
            
            self.analytics['last_updated'] = datetime.now().isoformat()
            self._save_analytics()
            
        except Exception as e:
            print(f"Analytics update error: {e}")
    
    def get_analytics(self) -> dict:
        """Get current analytics"""
        return self.analytics
    
    def _save_analytics(self):
        """Save analytics to file"""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics, f, indent=2)
        except Exception as e:
            print(f"Analytics save error: {e}")