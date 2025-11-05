# Research Assistant Workflow

This document explains how the Research Assistant works end-to-end.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Research Assistant                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐  │
│  │   Document   │────▶│    Vector    │────▶│     RAG      │  │
│  │  Ingestion   │     │    Store     │     │   Pipeline   │  │
│  └──────────────┘     └──────────────┘     └──────────────┘  │
│         │                     │                     │          │
│         ▼                     ▼                     ▼          │
│    Web Pages            ChromaDB +            OpenAI API       │
│       PDFs              Embeddings           LLM + Prompt      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                      CLI Interface                        │ │
│  │  ingest | research | clear | info                        │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Phase 1: Document Ingestion

```
User Input: research-assistant ingest https://example.com/article
                                  │
                                  ▼
                      ┌───────────────────────┐
                      │  Document Ingester    │
                      │  - Detect source type │
                      │  - Route to handler   │
                      └───────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
        ┌──────────────────┐        ┌──────────────────┐
        │ Web Page Handler │        │   PDF Handler    │
        │ - Fetch content  │        │ - Extract text   │
        │ - Parse HTML     │        │ - Per page       │
        │ - Clean text     │        │ - Page numbers   │
        └─────────┬────────┘        └────────┬─────────┘
                  │                          │
                  └──────────┬───────────────┘
                             ▼
                  ┌────────────────────┐
                  │  Document Object   │
                  │  + Metadata        │
                  │    - Source URL    │
                  │    - Title         │
                  │    - Page number   │
                  └──────────┬─────────┘
                             ▼
                  ┌────────────────────┐
                  │  Text Splitter     │
                  │  - Chunk size 1000 │
                  │  - Overlap 200     │
                  └──────────┬─────────┘
                             ▼
                  ┌────────────────────┐
                  │  OpenAI Embeddings │
                  │  (text-embedding-  │
                  │   ada-002)         │
                  └──────────┬─────────┘
                             ▼
                  ┌────────────────────┐
                  │    ChromaDB        │
                  │  Vector Storage    │
                  └────────────────────┘
```

### Phase 2: Research Query

```
User Input: research-assistant research "What is AI?"
                                  │
                                  ▼
                      ┌───────────────────────┐
                      │   RAG Pipeline        │
                      │   - Parse query       │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Query Embedding      │
                      │  (OpenAI Embeddings)  │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Similarity Search    │
                      │  - ChromaDB lookup    │
                      │  - Retrieve top K=5   │
                      │  - Get with scores    │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Source Retrieval     │
                      │  - Document chunks    │
                      │  - Metadata           │
                      │  - Relevance scores   │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Prompt Construction  │
                      │  - System prompt      │
                      │  - Sources [1][2]...  │
                      │  - User query         │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │   OpenAI LLM          │
                      │   (GPT-3.5-turbo)     │
                      │   - Generate summary  │
                      │   - Add citations     │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Research Brief       │
                      │  - Summary with [1]   │
                      │  - Source list        │
                      │  - URLs & excerpts    │
                      └───────────┬───────────┘
                                  ▼
                      ┌───────────────────────┐
                      │  Formatted Output     │
                      │  (Rich Console)       │
                      └───────────────────────┘
```

## Component Interactions

### 1. Configuration (config.py)
- Loads environment variables from `.env`
- Validates API keys
- Provides defaults for all settings
- Accessible to all components

### 2. Document Ingestion (ingestion.py)
- **WebPageIngester**: 
  - Uses `requests` to fetch HTML
  - Uses `BeautifulSoup` to parse and extract text
  - Removes scripts, styles, and cleans whitespace
- **PDFIngester**:
  - Uses `pypdf` to read PDF files
  - Extracts text page by page
  - Preserves page numbers for citations
- **DocumentIngester**: 
  - Routes to appropriate handler based on source

### 3. Vector Store (vector_store.py)
- **Text Splitting**:
  - Uses `RecursiveCharacterTextSplitter`
  - Creates overlapping chunks for context
  - Preserves metadata in each chunk
- **Embeddings**:
  - Uses OpenAI's `text-embedding-ada-002`
  - Converts text to 1536-dimensional vectors
- **ChromaDB**:
  - Persistent vector storage
  - Efficient similarity search
  - Metadata filtering

### 4. RAG Pipeline (rag_pipeline.py)
- **Retrieval**:
  - Embeds query
  - Searches ChromaDB for similar chunks
  - Returns top K results with scores
- **Generation**:
  - Constructs prompt with retrieved sources
  - Numbers sources [1], [2], etc.
  - Asks LLM to cite sources inline
  - Formats final research brief

### 5. Research Assistant (assistant.py)
- Orchestrates all components
- Provides high-level API
- Handles batch processing
- Error handling and logging

### 6. CLI (cli.py)
- User-friendly commands
- Rich console output
- Progress indicators
- File I/O support

## Example End-to-End Flow

```
1. User Command:
   $ research-assistant ingest https://en.wikipedia.org/wiki/AI

2. System Process:
   a. Fetch web page content
   b. Extract and clean text
   c. Split into chunks (1000 chars, 200 overlap)
   d. Generate embeddings for each chunk
   e. Store in ChromaDB with metadata

3. User Command:
   $ research-assistant research "What is artificial intelligence?"

4. System Process:
   a. Generate query embedding
   b. Search ChromaDB (top 5 matches)
   c. Retrieve relevant chunks + metadata
   d. Format sources for prompt
   e. Send to GPT-3.5-turbo with instructions
   f. Receive cited summary
   g. Format research brief with sources
   h. Display to user

5. Output:
   ================================================================================
   RESEARCH BRIEF: What is artificial intelligence?
   ================================================================================
   
   SUMMARY:
   --------------------------------------------------------------------------------
   Artificial intelligence (AI) is the intelligence of machines... [1]
   
   SOURCES:
   --------------------------------------------------------------------------------
   [1] Artificial intelligence
      URL: https://en.wikipedia.org/wiki/AI
      Excerpt: "Artificial intelligence (AI), in its broadest sense..."
   
   ================================================================================
```

## Performance Considerations

- **Embedding Caching**: ChromaDB stores embeddings permanently
- **Chunk Overlap**: Ensures context isn't lost at boundaries
- **Top-K Retrieval**: Balances quality vs. token usage
- **Batch Processing**: Multiple documents can be ingested together

## Error Handling

Each component has comprehensive error handling:
- Network errors during web scraping
- PDF parsing errors
- API rate limits
- Invalid configurations
- Missing files

All errors are logged with context and presented to users clearly.

## Extensibility

The modular design allows easy extension:
- Add new document types (Word, Excel, etc.)
- Swap vector databases (FAISS, Pinecone, etc.)
- Use different LLMs (Anthropic, local models)
- Add new CLI commands
- Implement web UI

## Security

- API keys stored in environment variables only
- No credentials in code or git
- Input validation throughout
- Permissions configured in CI/CD
- Dependencies regularly updated
