# Quick Start Guide

Get started with Research Assistant in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/jorgebjr28/research-assistant.git
cd research-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

3. **Set up your API key**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

Or export it directly:
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

## First Steps

### 1. Verify Installation
```bash
research-assistant --help
```

You should see the available commands:
- `ingest` - Add documents to your knowledge base
- `research` - Query and get cited summaries
- `clear` - Clear all documents
- `info` - View configuration

### 2. Ingest Your First Document

**From a web page:**
```bash
research-assistant ingest https://en.wikipedia.org/wiki/Artificial_intelligence
```

**From a PDF:**
```bash
research-assistant ingest /path/to/your/document.pdf
```

**Multiple sources at once:**
```bash
research-assistant ingest \
  https://en.wikipedia.org/wiki/Machine_learning \
  https://en.wikipedia.org/wiki/Deep_learning \
  research_paper.pdf
```

### 3. Research a Topic

```bash
research-assistant research "What is artificial intelligence?"
```

You'll get a formatted output like:
```
================================================================================
RESEARCH BRIEF: What is artificial intelligence?
================================================================================

SUMMARY:
--------------------------------------------------------------------------------
Artificial intelligence (AI) is... [1] This field encompasses various 
subfields including machine learning [2] and natural language processing...

SOURCES:
--------------------------------------------------------------------------------
[1] Artificial intelligence
   URL: https://en.wikipedia.org/wiki/Artificial_intelligence
   Excerpt: "Artificial intelligence (AI), in its broadest sense..."

[2] Machine learning
   URL: https://en.wikipedia.org/wiki/Machine_learning
   Excerpt: "Machine learning (ML) is a field of study..."

================================================================================
```

### 4. Save Results to a File

```bash
research-assistant research "Climate change impacts" -o report.txt
```

## Common Use Cases

### Academic Research
```bash
# Ingest papers and articles
research-assistant ingest paper1.pdf paper2.pdf paper3.pdf

# Research specific questions
research-assistant research "What are the latest findings on climate models?" -n 10
```

### Business Intelligence
```bash
# Ingest company reports and news
research-assistant ingest \
  https://company.com/annual-report \
  https://news-site.com/company-analysis \
  market_research.pdf

# Generate insights
research-assistant research "What are the company's growth strategies?"
```

### Technical Documentation
```bash
# Ingest documentation
research-assistant ingest \
  https://docs.python.org/3/tutorial/ \
  https://docs.python.org/3/library/

# Query specific topics
research-assistant research "How do Python decorators work?"
```

## Configuration

View your current configuration:
```bash
research-assistant info
```

Customize via environment variables in `.env`:
```bash
OPENAI_MODEL=gpt-4              # Use GPT-4 for better quality
TOP_K_RESULTS=10                # Retrieve more sources
CHUNK_SIZE=1500                 # Larger chunks for more context
TEMPERATURE=0.1                 # More deterministic responses
```

## Troubleshooting

### Issue: "OPENAI_API_KEY is required"
**Solution:** Make sure your API key is set:
```bash
export OPENAI_API_KEY='your-key-here'
```

### Issue: "No relevant sources found"
**Solution:** Ingest documents first:
```bash
research-assistant ingest <url-or-pdf>
```

### Issue: Import errors
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Next Steps

- 📚 Read the [full README](README.md) for detailed documentation
- 🐳 Try the [Docker setup](README.md#docker-installation)
- 💻 Explore [example scripts](examples/)
- 🔧 Customize your [configuration](.env.example)

## Need Help?

- Check the [README](README.md) for detailed documentation
- Open an [issue](https://github.com/jorgebjr28/research-assistant/issues) on GitHub

Happy researching! 🚀
