"""Document ingestion module for web pages and PDFs."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from urllib.parse import urlparse
import pypdf

logger = logging.getLogger(__name__)


class DocumentMetadata:
    """Metadata for ingested documents."""
    
    def __init__(
        self,
        source: str,
        source_type: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        page_number: Optional[int] = None
    ):
        self.source = source
        self.source_type = source_type
        self.title = title or source
        self.url = url or source
        self.page_number = page_number
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "source": self.source,
            "source_type": self.source_type,
            "title": self.title,
            "url": self.url,
            "page_number": self.page_number
        }


class Document:
    """Document with content and metadata."""
    
    def __init__(self, content: str, metadata: DocumentMetadata):
        self.content = content
        self.metadata = metadata


class WebPageIngester:
    """Ingest web pages."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def ingest(self, url: str) -> Document:
        """
        Ingest a web page from URL.
        
        Args:
            url: URL of the web page to ingest
            
        Returns:
            Document with extracted content and metadata
        """
        try:
            logger.info(f"Fetching web page: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else urlparse(url).netloc
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            content = '\n'.join(lines)
            
            metadata = DocumentMetadata(
                source=url,
                source_type="web",
                title=title,
                url=url
            )
            
            logger.info(f"Successfully ingested web page: {title}")
            return Document(content=content, metadata=metadata)
            
        except Exception as e:
            logger.error(f"Failed to ingest web page {url}: {str(e)}")
            raise


class PDFIngester:
    """Ingest PDF documents."""
    
    def ingest(self, file_path: str) -> List[Document]:
        """
        Ingest a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Documents (one per page)
        """
        try:
            logger.info(f"Ingesting PDF: {file_path}")
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            documents = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    text = page.extract_text()
                    
                    if text.strip():
                        metadata = DocumentMetadata(
                            source=file_path,
                            source_type="pdf",
                            title=path.name,
                            url=f"file://{path.absolute()}",
                            page_number=page_num
                        )
                        
                        documents.append(Document(content=text, metadata=metadata))
            
            logger.info(f"Successfully ingested PDF with {len(documents)} pages")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to ingest PDF {file_path}: {str(e)}")
            raise


class DocumentIngester:
    """Main document ingestion interface."""
    
    def __init__(self):
        self.web_ingester = WebPageIngester()
        self.pdf_ingester = PDFIngester()
    
    def ingest(self, source: str) -> List[Document]:
        """
        Ingest a document from URL or file path.
        
        Args:
            source: URL or file path
            
        Returns:
            List of ingested Documents
        """
        if source.startswith(('http://', 'https://')):
            return [self.web_ingester.ingest(source)]
        elif source.endswith('.pdf'):
            return self.pdf_ingester.ingest(source)
        else:
            raise ValueError(f"Unsupported source type: {source}")
