"""Main Research Assistant interface."""

import logging
from typing import List, Optional

from .config import Config, get_config
from .ingestion import DocumentIngester
from .vector_store import VectorStore
from .rag_pipeline import RAGPipeline, ResearchBrief

logger = logging.getLogger(__name__)


class ResearchAssistant:
    """Main Research Assistant with RAG capabilities."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the Research Assistant.
        
        Args:
            config: Optional configuration (defaults to loading from environment)
        """
        self.config = config or get_config()
        
        # Initialize components
        self.ingester = DocumentIngester()
        self.vector_store = VectorStore(self.config)
        self.rag_pipeline = RAGPipeline(self.config, self.vector_store)
        
        logger.info("Research Assistant initialized")
    
    def ingest_sources(self, sources: List[str]) -> None:
        """
        Ingest documents from URLs or file paths.
        
        Args:
            sources: List of URLs or file paths to ingest
        """
        logger.info(f"Ingesting {len(sources)} sources")
        
        for source in sources:
            try:
                logger.info(f"Processing: {source}")
                documents = self.ingester.ingest(source)
                self.vector_store.add_documents(documents)
                logger.info(f"Successfully ingested: {source}")
            except Exception as e:
                logger.error(f"Failed to ingest {source}: {str(e)}")
                # Continue with other sources
        
        logger.info("Ingestion complete")
    
    def research(self, query: str, num_sources: Optional[int] = None) -> ResearchBrief:
        """
        Conduct research on a query and generate a citation-aware brief.
        
        Args:
            query: Research query/topic
            num_sources: Number of sources to use (defaults to config setting)
            
        Returns:
            ResearchBrief with summary and citations
        """
        logger.info(f"Researching: {query}")
        return self.rag_pipeline.generate_research_brief(query, k=num_sources)
    
    def clear_knowledge_base(self) -> None:
        """Clear all ingested documents from the vector store."""
        logger.info("Clearing knowledge base")
        self.vector_store.clear()
        logger.info("Knowledge base cleared")
