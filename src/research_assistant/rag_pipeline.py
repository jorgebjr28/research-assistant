"""RAG pipeline for retrieval-augmented generation with citations."""

from typing import List, Dict, Any, Optional
from .vector_store import VectorStore
from .document_loader import DocumentLoader
import os


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline that retrieves relevant sources
    and synthesizes summaries with citations.
    """

    def __init__(self, vector_store: Optional[VectorStore] = None):
        """
        Initialize the RAG pipeline.
        
        Args:
            vector_store: Optional vector store instance. If None, creates a new one.
        """
        self.vector_store = vector_store or VectorStore()
        self.document_loader = DocumentLoader()

    def ingest_sources(self, sources: List[str]) -> Dict[str, Any]:
        """
        Ingest documents from sources (URLs or file paths) into the vector store.
        
        Args:
            sources: List of URLs or file paths
            
        Returns:
            Dictionary with ingestion statistics
        """
        documents = self.document_loader.load_multiple(sources)
        
        if not documents:
            return {
                'success': False,
                'message': 'No documents were successfully loaded',
                'documents_loaded': 0
            }
        
        self.vector_store.add_documents(documents)
        
        return {
            'success': True,
            'message': f'Successfully loaded {len(documents)} documents',
            'documents_loaded': len(documents),
            'sources': [doc['source'] for doc in documents]
        }

    def retrieve_sources(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant sources from the vector store.
        
        Args:
            query: Query text
            n_results: Number of results to retrieve
            
        Returns:
            List of retrieved documents with metadata
        """
        return self.vector_store.query(query, n_results)

    def _format_citation(self, metadata: Dict[str, Any], index: int) -> str:
        """
        Format a citation from metadata.
        
        Args:
            metadata: Document metadata
            index: Citation index number
            
        Returns:
            Formatted citation string
        """
        title = metadata.get('title', 'Unknown')
        source = metadata.get('source', 'Unknown')
        doc_type = metadata.get('type', 'document')
        
        return f"[{index}] {title} ({doc_type}): {source}"

    def _extract_excerpt(self, content: str, max_length: int = 200) -> str:
        """
        Extract a relevant excerpt from content.
        
        Args:
            content: Full content text
            max_length: Maximum length of excerpt
            
        Returns:
            Excerpt string
        """
        if len(content) <= max_length:
            return content
        
        # Try to break at sentence boundary
        excerpt = content[:max_length]
        last_period = excerpt.rfind('.')
        last_newline = excerpt.rfind('\n')
        break_point = max(last_period, last_newline)
        
        if break_point > max_length * 0.5:
            excerpt = excerpt[:break_point + 1]
        else:
            excerpt = excerpt + "..."
        
        return excerpt.strip()

    def synthesize_research_brief(self, topic: str, n_sources: int = 5) -> Dict[str, Any]:
        """
        Create a comprehensive research brief on a topic with citations.
        
        Args:
            topic: Research topic/query
            n_sources: Number of sources to retrieve
            
        Returns:
            Dictionary containing the research brief with citations
        """
        # Retrieve relevant sources
        retrieved_docs = self.retrieve_sources(topic, n_sources)
        
        if not retrieved_docs:
            return {
                'topic': topic,
                'summary': 'No relevant sources found. Please ingest documents first.',
                'citations': [],
                'excerpts': []
            }
        
        # Group by source to avoid duplicate citations
        source_map = {}
        for doc in retrieved_docs:
            source = doc['metadata'].get('source', 'Unknown')
            if source not in source_map:
                source_map[source] = {
                    'metadata': doc['metadata'],
                    'contents': []
                }
            source_map[source]['contents'].append(doc['content'])
        
        # Create citations
        citations = []
        excerpts = []
        summary_parts = []
        
        for idx, (source, data) in enumerate(source_map.items(), 1):
            citation = self._format_citation(data['metadata'], idx)
            citations.append(citation)
            
            # Create excerpts from the most relevant content
            for content in data['contents'][:2]:  # Limit to 2 excerpts per source
                excerpt = self._extract_excerpt(content)
                excerpts.append({
                    'citation_index': idx,
                    'text': excerpt
                })
            
            # Build summary parts
            title = data['metadata'].get('title', 'Source')
            excerpt_text = self._extract_excerpt(data['contents'][0], 300)
            summary_parts.append(f"According to {title} [{idx}], {excerpt_text}")
        
        # Construct the summary
        summary = f"# Research Brief: {topic}\n\n"
        summary += "## Overview\n\n"
        summary += f"This research brief synthesizes information from {len(source_map)} source(s) "
        summary += f"related to '{topic}'.\n\n"
        summary += "## Key Findings\n\n"
        
        for part in summary_parts:
            summary += f"- {part}\n\n"
        
        summary += "## Sources\n\n"
        for citation in citations:
            summary += f"{citation}\n"
        
        return {
            'topic': topic,
            'summary': summary,
            'citations': citations,
            'excerpts': excerpts,
            'num_sources': len(source_map)
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG pipeline."""
        return self.vector_store.get_stats()
