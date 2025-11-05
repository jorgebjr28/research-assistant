"""Vector store management using ChromaDB."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import os


class VectorStore:
    """Manages vector database for document storage and retrieval."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("research_documents")
        except:
            self.collection = self.client.create_collection(
                name="research_documents",
                metadata={"description": "Research documents with citations"}
            )

    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only break if it's not too early
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Remove empty chunks

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of document dictionaries with 'content', 'source', 'title', 'type'
        """
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for doc_idx, doc in enumerate(documents):
            content = doc['content']
            chunks = self._chunk_text(content)
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = f"doc_{doc_idx}_chunk_{chunk_idx}"
                all_chunks.append(chunk)
                all_ids.append(chunk_id)
                all_metadatas.append({
                    'source': doc['source'],
                    'title': doc['title'],
                    'type': doc['type'],
                    'chunk_index': chunk_idx,
                    'total_chunks': len(chunks)
                })
        
        if all_chunks:
            # Generate embeddings
            embeddings = self.embedding_model.encode(all_chunks).tolist()
            
            # Add to collection
            self.collection.add(
                documents=all_chunks,
                embeddings=embeddings,
                metadatas=all_metadatas,
                ids=all_ids
            )

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector store for relevant documents.
        
        Args:
            query_text: The query text
            n_results: Number of results to return
            
        Returns:
            List of retrieved documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query_text]).tolist()
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        # Format results
        retrieved_docs = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'id': results['ids'][0][i] if results['ids'] else None
                })
        
        return retrieved_docs

    def clear(self) -> None:
        """Clear all documents from the vector store."""
        # Delete and recreate collection
        self.client.delete_collection("research_documents")
        self.collection = self.client.create_collection(
            name="research_documents",
            metadata={"description": "Research documents with citations"}
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        count = self.collection.count()
        return {
            'total_chunks': count,
            'persist_directory': self.persist_directory
        }
