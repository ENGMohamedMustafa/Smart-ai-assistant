import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from services.whisper_service import WhisperService
from services.translation_service import TranslationService
from services.rag_service import RAGService
from services.dalle_service import DalleService

class TestWhisperService:
    def test_transcribe_success(self):
        # Mock OpenAI response
        with patch('openai.Audio.transcribe') as mock_transcribe:
            mock_transcribe.return_value.text = "Hello world"
            
            service = WhisperService()
            result = service.transcribe("dummy_path.wav")
            
            assert result == "Hello world"
    
    def test_transcribe_failure(self):
        with patch('openai.Audio.transcribe', side_effect=Exception("API Error")):
            service = WhisperService()
            result = service.transcribe("dummy_path.wav")
            
            assert result is None

class TestTranslationService:
    def test_translate_success(self):
        service = TranslationService()
        # Mock successful translation
        with patch.object(service.translator, 'translate') as mock_translate:
            mock_result = Mock()
            mock_result.text = "مرحبا بالعالم"
            mock_translate.return_value = mock_result
            
            result = service.translate("Hello world", "Arabic")
            assert result == "مرحبا بالعالم"
    
    def test_detect_language(self):
        service = TranslationService()
        with patch.object(service.translator, 'detect') as mock_detect:
            mock_result = Mock()
            mock_result.lang = 'en'
            mock_detect.return_value = mock_result
            
            result = service.detect_language("Hello world")
            assert result == 'en'

class TestRAGService:
    def test_get_response(self):
        with patch('langchain.vectorstores.FAISS.from_texts'):
            service = RAGService()
            service.qa_chain = Mock()
            service.qa_chain.run.return_value = "Test response"
            
            result = service.get_response("Test query")
            assert result == "Test response"

class TestDalleService:
    def test_generate_image(self):
        with patch('openai.Image.create') as mock_create:
            mock_response = Mock()
            mock_response.data = [Mock()]
            mock_response.data[0].url = "https://example.com/image.png"
            mock_create.return_value = mock_response
            
            service = DalleService()
            result = service.generate_image("A beautiful sunset")
            
            assert result == "https://example.com/image.png"