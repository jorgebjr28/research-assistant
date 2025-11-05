"""Tests for document ingestion."""

import pytest
from pathlib import Path
from research_assistant.ingestion import (
    DocumentMetadata,
    Document,
    DocumentIngester
)


def test_document_metadata():
    """Test DocumentMetadata creation and serialization."""
    metadata = DocumentMetadata(
        source="test.pdf",
        source_type="pdf",
        title="Test Document",
        url="file://test.pdf",
        page_number=1
    )
    
    assert metadata.source == "test.pdf"
    assert metadata.source_type == "pdf"
    assert metadata.title == "Test Document"
    assert metadata.page_number == 1
    
    # Test to_dict
    metadata_dict = metadata.to_dict()
    assert metadata_dict["source"] == "test.pdf"
    assert metadata_dict["title"] == "Test Document"


def test_document_creation():
    """Test Document creation."""
    metadata = DocumentMetadata(
        source="test.txt",
        source_type="text",
        title="Test"
    )
    
    doc = Document(content="Test content", metadata=metadata)
    
    assert doc.content == "Test content"
    assert doc.metadata.source == "test.txt"


def test_document_ingester_initialization():
    """Test DocumentIngester initialization."""
    ingester = DocumentIngester()
    
    assert ingester.web_ingester is not None
    assert ingester.pdf_ingester is not None


def test_document_ingester_invalid_source():
    """Test DocumentIngester with unsupported source."""
    ingester = DocumentIngester()
    
    with pytest.raises(ValueError, match="Unsupported source type"):
        ingester.ingest("unsupported.txt")
