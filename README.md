# Research Assistant with RAG & Citation-Aware Summaries

A powerful command-line research assistant that uses Retrieval-Augmented Generation (RAG) to synthesize information from web pages and PDFs, providing organized research briefs with citations and excerpts.

## Features

- 📚 **Multi-Source Ingestion**: Load documents from web pages (HTML) and PDFs
- 🔍 **Vector Database**: Efficient storage and retrieval using ChromaDB
- 🤖 **RAG Pipeline**: Retrieve relevant sources and synthesize summaries
- 📝 **Citation-Aware**: Automatic citation generation with source tracking
- 📖 **Excerpt Extraction**: Pull relevant excerpts from source materials
- 💻 **CLI Interface**: Easy-to-use command-line interface

## Technology Stack

- **Python 3.8+**
- **FAISS**: Fast vector similarity search for document retrieval
- **Sentence Transformers**: For generating embeddings
- **BeautifulSoup4**: Web scraping and HTML parsing
- **PyPDF**: PDF document parsing
- **Requests**: HTTP client for fetching web content

## Installation

### Option 1: Install with pip (Recommended)

```bash
git clone https://github.com/jorgebjr28/research-assistant.git
cd research-assistant
pip install -e .
```

After installation, you can use the `research-assistant` command directly:
```bash
research-assistant ingest document.txt
research-assistant query "your topic"
```

### Option 2: Install dependencies only

```bash
git clone https://github.com/jorgebjr28/research-assistant.git
cd research-assistant
pip install -r requirements.txt
```

Then use the script directly:
```bash
python research_assistant.py ingest document.txt
python research_assistant.py query "your topic"
```

## Usage

The research assistant provides a CLI with several commands:

### 1. Ingest Documents

Load documents from URLs or local file paths into the vector database:

```bash
python research_assistant.py ingest https://example.com/article1.html https://example.com/article2.pdf
```

### 2. Query/Research a Topic

Generate a research brief on any topic:

```bash
python research_assistant.py query "machine learning applications"
```

With options:
```bash
python research_assistant.py query "climate change" --num-sources 10 --show-excerpts
```

Options:
- `--num-sources N`: Number of sources to retrieve (default: 5)
- `--show-excerpts`: Show detailed excerpts from each source

### 3. View Statistics

Check the current state of your vector database:

```bash
python research_assistant.py stats
```

### 4. Clear Database

Remove all documents from the vector store:

```bash
python research_assistant.py clear
```

Or skip the confirmation prompt:
```bash
python research_assistant.py clear --force
```

## Quick Start Demo

Run the included example script to see the research assistant in action:

```bash
./example_usage.sh
```

This will demonstrate the complete workflow: ingesting documents, querying topics, and viewing results with citations.

## Example Workflow

```bash
# Set environment variable for offline mode (optional)
export USE_SENTENCE_TRANSFORMERS=false

# 1. Ingest some research sources (local files or URLs)
python research_assistant.py ingest \
  /path/to/document1.txt \
  /path/to/document2.pdf

# 2. Query on a topic
python research_assistant.py query "What is artificial intelligence?" --num-sources 3

# 3. Query with detailed excerpts
python research_assistant.py query "machine learning applications" --show-excerpts

# 4. Check statistics
python research_assistant.py stats
```

## How It Works

1. **Document Ingestion**: 
   - Documents are loaded from URLs or files
   - Text is extracted from HTML (using BeautifulSoup) or PDFs (using PyPDF)
   - Content is chunked into smaller segments with overlap

2. **Vector Storage**:
   - Text chunks are embedded using Sentence Transformers
   - Embeddings are stored in FAISS index with metadata (source, title, type)

3. **Retrieval**:
   - User queries are embedded using the same model
   - Similar chunks are retrieved using vector similarity search

4. **Synthesis**:
   - Retrieved chunks are organized by source
   - Citations are generated with proper formatting
   - Excerpts are extracted and attributed
   - A comprehensive research brief is generated

## Project Structure

```
research-assistant/
├── src/
│   └── research_assistant/
│       ├── __init__.py
│       ├── document_loader.py    # Load web pages and PDFs
│       ├── vector_store.py       # ChromaDB vector database
│       ├── rag_pipeline.py       # RAG pipeline with citations
│       └── cli.py                # Command-line interface
├── research_assistant.py         # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Configuration

The vector database is stored in `./faiss_index` by default. This directory is created automatically and persists between sessions.

### Environment Variables

- `USE_SENTENCE_TRANSFORMERS`: Set to `false` to use TF-IDF embeddings instead of Sentence Transformers (useful for offline environments or when HuggingFace models aren't available)

```bash
export USE_SENTENCE_TRANSFORMERS=false
```

### Embedding Models

The system supports two embedding approaches:

1. **Sentence Transformers** (default): Uses the `all-MiniLM-L6-v2` model for high-quality embeddings
   - Requires internet connection on first use to download model
   - Provides better semantic understanding

2. **TF-IDF** (fallback): Uses sklearn's TfidfVectorizer
   - Works completely offline
   - No model downloads required
   - Good for keyword-based retrieval

## Error Handling

- Failed document loads are skipped with error messages
- Empty queries return helpful messages
- The CLI provides clear error messages for common issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Credits

Forked from: [custom-ai-agent](https://github.com/jorgebjr28/custom-ai-agent)
