"""Document loading functionality for web pages and PDFs."""

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from typing import List, Dict, Any
from urllib.parse import urlparse
import io


class DocumentLoader:
    """Load and parse documents from various sources."""

    @staticmethod
    def load_from_url(url: str) -> Dict[str, Any]:
        """
        Load content from a web URL.
        
        Args:
            url: The URL to load content from
            
        Returns:
            Dictionary containing content and metadata
        """
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            # Check if it's a PDF
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                return DocumentLoader._load_pdf_from_bytes(response.content, url)
            
            # Otherwise parse as HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Get title
            title = soup.title.string if soup.title else urlparse(url).netloc
            
            return {
                'content': text,
                'source': url,
                'title': title,
                'type': 'webpage'
            }
        except Exception as e:
            return {
                'content': '',
                'source': url,
                'title': '',
                'type': 'error',
                'error': str(e)
            }

    @staticmethod
    def _load_pdf_from_bytes(pdf_bytes: bytes, source: str) -> Dict[str, Any]:
        """
        Load PDF from bytes.
        
        Args:
            pdf_bytes: PDF file content as bytes
            source: Source identifier (URL or file path)
            
        Returns:
            Dictionary containing content and metadata
        """
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Get metadata
            metadata = reader.metadata if reader.metadata else {}
            title = metadata.get('/Title', source) if metadata else source
            
            return {
                'content': text.strip(),
                'source': source,
                'title': str(title),
                'type': 'pdf'
            }
        except Exception as e:
            return {
                'content': '',
                'source': source,
                'title': '',
                'type': 'error',
                'error': str(e)
            }

    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]:
        """
        Load content from a local file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing content and metadata
        """
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as f:
                    return DocumentLoader._load_pdf_from_bytes(f.read(), file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    'content': content,
                    'source': file_path,
                    'title': file_path.split('/')[-1],
                    'type': 'file'
                }
        except Exception as e:
            return {
                'content': '',
                'source': file_path,
                'title': '',
                'type': 'error',
                'error': str(e)
            }

    @staticmethod
    def load_multiple(sources: List[str]) -> List[Dict[str, Any]]:
        """
        Load multiple documents from various sources.
        
        Args:
            sources: List of URLs or file paths
            
        Returns:
            List of document dictionaries
        """
        documents = []
        for source in sources:
            if source.startswith('http://') or source.startswith('https://'):
                doc = DocumentLoader.load_from_url(source)
            else:
                doc = DocumentLoader.load_from_file(source)
            
            if doc['content']:  # Only add if content was loaded successfully
                documents.append(doc)
        
        return documents
