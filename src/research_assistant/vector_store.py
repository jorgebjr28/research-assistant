"""Vector store implementation using ChromaDB."""

import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document as LangChainDocument

from .config import Config
from .ingestion import Document

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store for document embeddings using ChromaDB."""
    
    def __init__(self, config: Config):
        """
        Initialize the vector store.
        
        Args:
            config: Application configuration
        """
        self.config = config
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=config.openai_api_key,
            model=config.embedding_model
        )
        
        # Create ChromaDB directory if it doesn't exist
        self.config.chroma_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
        )
        
        # Initialize Chroma vector store
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embeddings,
            persist_directory=str(config.chroma_db_path),
        )
        
        logger.info(f"Initialized vector store at {config.chroma_db_path}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Documents to add
        """
        try:
            # Convert to LangChain documents and split
            langchain_docs = []
            
            for doc in documents:
                # Create LangChain document
                lc_doc = LangChainDocument(
                    page_content=doc.content,
                    metadata=doc.metadata.to_dict()
                )
                langchain_docs.append(lc_doc)
            
            # Split documents into chunks
            split_docs = self.text_splitter.split_documents(langchain_docs)
            
            logger.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")
            
            # Add to vector store
            self.vector_store.add_documents(split_docs)
            
            logger.info(f"Successfully added {len(split_docs)} chunks to vector store")
            
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {str(e)}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return (defaults to config.top_k_results)
            
        Returns:
            List of documents with content and metadata
        """
        try:
            k = k or self.config.top_k_results
            
            logger.info(f"Searching for: {query}")
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": float(score)
                })
            
            logger.info(f"Found {len(formatted_results)} relevant chunks")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    def clear(self) -> None:
        """Clear all documents from the vector store."""
        try:
            # Delete and recreate the collection
            self.vector_store.delete_collection()
            
            self.vector_store = Chroma(
                collection_name=self.config.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.config.chroma_db_path),
            )
            
            logger.info("Cleared vector store")
            
        except Exception as e:
            logger.error(f"Failed to clear vector store: {str(e)}")
            raise
