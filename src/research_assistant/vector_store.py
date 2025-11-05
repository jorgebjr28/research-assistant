"""Vector store management using FAISS."""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer


class VectorStore:
    """Manages vector database for document storage and retrieval."""

    def __init__(self, persist_directory: str = "./faiss_index"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # File paths
        self.index_file = os.path.join(persist_directory, "index.faiss")
        self.metadata_file = os.path.join(persist_directory, "metadata.pkl")
        
        # Initialize embedding model - Try sentence-transformers, fall back to TF-IDF
        self.use_tfidf = False
        self.embedding_model = None
        
        # Check if we should skip sentence-transformers (e.g., in offline environments)
        use_st = os.environ.get('USE_SENTENCE_TRANSFORMERS', 'auto').lower()
        
        if use_st != 'false':
            try:
                # Set timeout for HuggingFace downloads
                os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '10'
                
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.dimension = 384  # Dimension for all-MiniLM-L6-v2
            except Exception as e:
                # Fallback to TF-IDF
                if use_st == 'auto':
                    print("Note: Using TF-IDF for embeddings (SentenceTransformers unavailable)")
                    self._init_tfidf()
                else:
                    raise
        else:
            # Explicitly use TF-IDF
            self._init_tfidf()
        
        # Initialize or load index
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadatas = data['metadatas']
                self.ids = data['ids']
                if 'use_tfidf' in data:
                    self.use_tfidf = data['use_tfidf']
                    if self.use_tfidf and 'vectorizer' in data:
                        self.vectorizer = data['vectorizer']
                        self.dimension = data['dimension']
                        self.tfidf_fitted = True
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
            self.metadatas = []
            self.ids = []
    
    def _init_tfidf(self):
        """Initialize TF-IDF vectorizer as fallback."""
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.dimension = 384
        self.use_tfidf = True
        self.tfidf_fitted = False

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
        
        base_idx = len(self.documents)
        
        for doc_idx, doc in enumerate(documents):
            content = doc['content']
            chunks = self._chunk_text(content)
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = f"doc_{base_idx + doc_idx}_chunk_{chunk_idx}"
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
            if self.use_tfidf:
                # Fit vectorizer on all documents (first time or refit)
                all_docs = self.documents + all_chunks
                tfidf_matrix = self.vectorizer.fit_transform(all_docs)
                self.tfidf_fitted = True
                
                # Update dimension if it changed
                new_dimension = tfidf_matrix.shape[1]
                if new_dimension != self.dimension:
                    self.dimension = new_dimension
                    self.index = faiss.IndexFlatL2(self.dimension)
                
                # Get embeddings for new chunks
                start_idx = len(self.documents)
                embeddings_np = tfidf_matrix[start_idx:].toarray().astype('float32')
                
                # Re-index ALL documents with new vectorizer (to ensure consistency)
                if len(self.documents) > 0:
                    old_embeddings = tfidf_matrix[:start_idx].toarray().astype('float32')
                    self.index = faiss.IndexFlatL2(self.dimension)
                    self.index.add(old_embeddings)
            else:
                embeddings = self.embedding_model.encode(all_chunks)
                embeddings_np = np.array(embeddings).astype('float32')
            
            # Add to index
            self.index.add(embeddings_np)
            
            # Store documents and metadata
            self.documents.extend(all_chunks)
            self.metadatas.extend(all_metadatas)
            self.ids.extend(all_ids)
            
            # Persist
            self._save()

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector store for relevant documents.
        
        Args:
            query_text: The query text
            n_results: Number of results to return
            
        Returns:
            List of retrieved documents with metadata
        """
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        if self.use_tfidf:
            if not self.tfidf_fitted:
                return []
            query_vec = self.vectorizer.transform([query_text]).toarray().astype('float32')
        else:
            query_embedding = self.embedding_model.encode([query_text])
            query_vec = np.array(query_embedding).astype('float32')
        
        # Search the index
        k = min(n_results, self.index.ntotal)
        distances, indices = self.index.search(query_vec, k)
        
        # Format results
        retrieved_docs = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                retrieved_docs.append({
                    'content': self.documents[idx],
                    'metadata': self.metadatas[idx],
                    'distance': float(distances[0][i]),
                    'id': self.ids[idx]
                })
        
        return retrieved_docs

    def _save(self) -> None:
        """Save the index and metadata to disk."""
        faiss.write_index(self.index, self.index_file)
        data = {
            'documents': self.documents,
            'metadatas': self.metadatas,
            'ids': self.ids,
            'use_tfidf': self.use_tfidf,
            'dimension': self.dimension
        }
        if self.use_tfidf:
            data['vectorizer'] = self.vectorizer
        
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(data, f)

    def clear(self) -> None:
        """Clear all documents from the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadatas = []
        self.ids = []
        self._save()

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        return {
            'total_chunks': self.index.ntotal,
            'persist_directory': self.persist_directory
        }
