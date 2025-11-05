# Research Assistant with RAG & Citation-Aware Summaries

A powerful research assistant that uses Retrieval-Augmented Generation (RAG) to provide well-cited summaries from web pages and PDF documents. Built with LangChain, ChromaDB, and OpenAI.

## Features

- 🌐 **Web Page Ingestion**: Extract and process content from any web page
- 📄 **PDF Support**: Ingest and process PDF documents
- 🔍 **Vector Search**: Fast similarity search using ChromaDB with OpenAI embeddings
- 🤖 **RAG Pipeline**: Retrieve relevant sources and synthesize citation-aware summaries
- 📚 **Source Provenance**: Every claim is backed by citations with clickable links
- 💻 **CLI Interface**: Easy-to-use command-line interface
- 🐳 **Docker Support**: Containerized deployment ready

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/jorgebjr28/research-assistant.git
cd research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Docker Installation

1. Build the Docker image:
```bash
docker-compose build
```

2. Create a `.env` file with your configuration (see `.env.example`)

## Usage

### CLI Commands

#### Ingest Documents

Ingest web pages:
```bash
research-assistant ingest https://example.com/article
```

Ingest PDF files:
```bash
research-assistant ingest document.pdf
```

Ingest multiple sources:
```bash
research-assistant ingest https://site1.com https://site2.com doc1.pdf doc2.pdf
```

#### Research Topics

Generate a research brief:
```bash
research-assistant research "What are the benefits of artificial intelligence?"
```

Specify number of sources to use:
```bash
research-assistant research "Climate change impacts" -n 10
```

Save output to file:
```bash
research-assistant research "Machine learning trends" -o report.txt
```

#### Manage Knowledge Base

View configuration:
```bash
research-assistant info
```

Clear all documents:
```bash
research-assistant clear
```

### Docker Usage

Run with Docker Compose:
```bash
# Ingest documents
docker-compose run research-assistant ingest https://example.com/article

# Research a topic
docker-compose run research-assistant research "Your query here"
```

## Architecture

The Research Assistant consists of several key components:

### 1. Document Ingestion (`ingestion.py`)
- **WebPageIngester**: Fetches and extracts text from web pages using BeautifulSoup
- **PDFIngester**: Extracts text from PDF files using pypdf
- **DocumentIngester**: Unified interface for all document types

### 2. Vector Store (`vector_store.py`)
- Uses ChromaDB for efficient vector storage and similarity search
- Splits documents into chunks with overlap for better context
- OpenAI embeddings for semantic search

### 3. RAG Pipeline (`rag_pipeline.py`)
- Retrieves relevant document chunks for a query
- Synthesizes citation-aware summaries using OpenAI models
- Tracks source provenance with clickable links and excerpts

### 4. Research Assistant (`assistant.py`)
- Main interface orchestrating all components
- Manages document ingestion and research workflows

### 5. CLI (`cli.py`)
- User-friendly command-line interface
- Rich console output with colors and formatting

## Configuration

Configuration is managed through environment variables or a `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model for summarization |
| `EMBEDDING_MODEL` | `text-embedding-ada-002` | Model for embeddings |
| `CHROMA_DB_PATH` | `./data/chroma_db` | Path to ChromaDB storage |
| `COLLECTION_NAME` | `research_docs` | ChromaDB collection name |
| `CHUNK_SIZE` | `1000` | Text chunk size for splitting |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K_RESULTS` | `5` | Number of sources to retrieve |
| `TEMPERATURE` | `0.3` | LLM temperature (0-1) |

## Example Workflow

1. **Ingest sources**:
```bash
research-assistant ingest \
  https://en.wikipedia.org/wiki/Artificial_intelligence \
  https://en.wikipedia.org/wiki/Machine_learning \
  ai_paper.pdf
```

2. **Research a topic**:
```bash
research-assistant research "What is the difference between AI and machine learning?"
```

3. **Output**: You'll receive a formatted research brief with:
   - A comprehensive summary
   - Inline citations [1], [2], etc.
   - Full source list with URLs and excerpts

## Development

### Project Structure
```
research-assistant/
├── src/
│   └── research_assistant/
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       ├── ingestion.py       # Document ingestion
│       ├── vector_store.py    # ChromaDB integration
│       ├── rag_pipeline.py    # RAG with citations
│       ├── assistant.py       # Main interface
│       └── cli.py             # CLI commands
├── tests/                     # Test files
├── data/                      # Data storage (gitignored)
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── Dockerfile                 # Docker image
├── docker-compose.yml         # Docker Compose config
└── README.md                  # This file
```

### Running Tests

```bash
pytest tests/
```

## Tech Stack

- **Python 3.8+**: Core language
- **LangChain**: RAG framework and utilities
- **ChromaDB**: Vector database for embeddings
- **OpenAI**: LLM and embedding models
- **BeautifulSoup4**: Web scraping
- **pypdf**: PDF processing
- **Click**: CLI framework
- **Rich**: Beautiful console output
- **Docker**: Containerization

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Based on concepts from the custom-ai-agent repository and modern RAG practices.
