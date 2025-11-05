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

1. Clone the repository:
```bash
git clone https://github.com/jorgebjr28/research-assistant.git
cd research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
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

## Example Workflow

```bash
# 1. Ingest some research sources
python research_assistant.py ingest \
  https://en.wikipedia.org/wiki/Artificial_intelligence \
  https://en.wikipedia.org/wiki/Machine_learning

# 2. Query on a topic
python research_assistant.py query "What is artificial intelligence?" --num-sources 3

# 3. Check statistics
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
