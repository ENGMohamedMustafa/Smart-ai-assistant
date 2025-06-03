import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def sample_text_file(temp_dir):
    """Create sample text file for testing"""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("This is a sample document for testing RAG functionality.")
    return file_path

@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock OpenAI API key"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")