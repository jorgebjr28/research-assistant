"""Tests for configuration."""

import pytest
import os
from pathlib import Path
from research_assistant.config import Config


def test_config_defaults():
    """Test Config with default values."""
    # Set required env var
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    config = Config()
    
    assert config.openai_api_key == "test-key"
    assert config.openai_model == "gpt-3.5-turbo"
    assert config.embedding_model == "text-embedding-ada-002"
    assert config.chunk_size == 1000
    assert config.chunk_overlap == 200
    assert config.top_k_results == 5
    assert config.temperature == 0.3


def test_config_validation_missing_key():
    """Test Config validation with missing API key."""
    # Clear the API key
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    config = Config()
    
    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        config.validate_config()


def test_config_validation_success():
    """Test Config validation with valid key."""
    os.environ["OPENAI_API_KEY"] = "valid-key"
    
    config = Config()
    assert config.validate_config() is True
