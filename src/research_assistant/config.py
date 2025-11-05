"""Configuration management for Research Assistant."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseModel):
    """Configuration settings for the Research Assistant."""
    
    # OpenAI API Configuration
    openai_api_key: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    openai_model: str = Field(
        default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    )
    
    # Vector Database Configuration
    chroma_db_path: Path = Field(
        default_factory=lambda: Path(os.getenv("CHROMA_DB_PATH", "./data/chroma_db"))
    )
    collection_name: str = Field(
        default_factory=lambda: os.getenv("COLLECTION_NAME", "research_docs")
    )
    
    # Embedding Configuration
    embedding_model: str = Field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    )
    
    # RAG Configuration
    chunk_size: int = Field(
        default_factory=lambda: int(os.getenv("CHUNK_SIZE", "1000"))
    )
    chunk_overlap: int = Field(
        default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "200"))
    )
    top_k_results: int = Field(
        default_factory=lambda: int(os.getenv("TOP_K_RESULTS", "5"))
    )
    
    # Temperature for generation
    temperature: float = Field(
        default_factory=lambda: float(os.getenv("TEMPERATURE", "0.3"))
    )
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required. Set it in .env file or environment variable."
            )
        return True
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True


def get_config() -> Config:
    """Get the application configuration."""
    config = Config()
    config.validate_config()
    return config
