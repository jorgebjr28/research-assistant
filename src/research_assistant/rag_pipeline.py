"""RAG pipeline with citation-aware summaries."""

import logging
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from .config import Config
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class Citation:
    """Citation information for a source."""
    
    def __init__(self, source: str, title: str, url: str, excerpt: str, page_number: Optional[int] = None):
        self.source = source
        self.title = title
        self.url = url
        self.excerpt = excerpt
        self.page_number = page_number
    
    def format(self, index: int) -> str:
        """Format citation for display."""
        page_info = f", p. {self.page_number}" if self.page_number else ""
        return f"[{index}] {self.title}{page_info}\n   URL: {self.url}\n   Excerpt: \"{self.excerpt[:150]}...\""


class ResearchBrief:
    """A research brief with summary and citations."""
    
    def __init__(self, query: str, summary: str, citations: List[Citation]):
        self.query = query
        self.summary = summary
        self.citations = citations
    
    def format(self) -> str:
        """Format the research brief for display."""
        output = []
        output.append("=" * 80)
        output.append(f"RESEARCH BRIEF: {self.query}")
        output.append("=" * 80)
        output.append("")
        output.append("SUMMARY:")
        output.append("-" * 80)
        output.append(self.summary)
        output.append("")
        
        if self.citations:
            output.append("SOURCES:")
            output.append("-" * 80)
            for i, citation in enumerate(self.citations, start=1):
                output.append(citation.format(i))
                output.append("")
        
        output.append("=" * 80)
        return "\n".join(output)


class RAGPipeline:
    """RAG pipeline for generating citation-aware research summaries."""
    
    def __init__(self, config: Config, vector_store: VectorStore):
        """
        Initialize the RAG pipeline.
        
        Args:
            config: Application configuration
            vector_store: Vector store for retrieval
        """
        self.config = config
        self.vector_store = vector_store
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=config.openai_api_key,
            model_name=config.openai_model,
            temperature=config.temperature
        )
        
        # Create prompt template
        self.system_prompt = """You are a research assistant that provides accurate, well-cited summaries.

Your task is to synthesize information from the provided sources to answer the user's query.

IMPORTANT INSTRUCTIONS:
1. Base your answer ONLY on the provided sources
2. Use inline citations like [1], [2], etc. to reference sources
3. Each factual claim should have a citation
4. Be objective and precise
5. If sources don't fully answer the query, acknowledge the limitations
6. Organize information clearly with good structure

The sources are numbered and provided below."""

        self.human_prompt_template = """QUERY: {query}

SOURCES:
{sources}

Please provide a comprehensive, well-organized summary that answers the query using the sources above. Use inline citations [1], [2], etc. to reference specific sources."""
        
        logger.info("Initialized RAG pipeline")
    
    def _format_sources(self, results: List[Dict[str, Any]]) -> str:
        """Format retrieved sources for the prompt."""
        formatted = []
        for i, result in enumerate(results, start=1):
            metadata = result["metadata"]
            content = result["content"]
            
            title = metadata.get("title", "Unknown")
            page_num = metadata.get("page_number")
            page_info = f" (Page {page_num})" if page_num else ""
            
            formatted.append(f"[{i}] {title}{page_info}")
            formatted.append(f"Content: {content}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _extract_citations(self, results: List[Dict[str, Any]]) -> List[Citation]:
        """Extract citation objects from results."""
        citations = []
        for result in results:
            metadata = result["metadata"]
            content = result["content"]
            
            citation = Citation(
                source=metadata.get("source", "Unknown"),
                title=metadata.get("title", "Unknown"),
                url=metadata.get("url", ""),
                excerpt=content,
                page_number=metadata.get("page_number")
            )
            citations.append(citation)
        
        return citations
    
    def generate_research_brief(self, query: str, k: Optional[int] = None) -> ResearchBrief:
        """
        Generate a research brief for the given query.
        
        Args:
            query: Research query
            k: Number of sources to retrieve (defaults to config.top_k_results)
            
        Returns:
            ResearchBrief with summary and citations
        """
        try:
            logger.info(f"Generating research brief for: {query}")
            
            # Retrieve relevant documents
            results = self.vector_store.similarity_search(query, k=k)
            
            if not results:
                logger.warning("No relevant documents found")
                return ResearchBrief(
                    query=query,
                    summary="No relevant sources found to answer this query. Please ingest relevant documents first.",
                    citations=[]
                )
            
            # Format sources for prompt
            sources_text = self._format_sources(results)
            
            # Create messages
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=self.human_prompt_template.format(
                    query=query,
                    sources=sources_text
                ))
            ]
            
            # Generate summary
            logger.info("Generating summary with LLM")
            response = self.llm.invoke(messages)
            summary = response.content
            
            # Extract citations
            citations = self._extract_citations(results)
            
            # Create research brief
            brief = ResearchBrief(
                query=query,
                summary=summary,
                citations=citations
            )
            
            logger.info("Successfully generated research brief")
            return brief
            
        except Exception as e:
            logger.error(f"Failed to generate research brief: {str(e)}")
            raise
