# Examples

This directory contains example scripts demonstrating the Research Assistant functionality.

## Running Examples

1. Make sure you have set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

2. Run the example:
```bash
python examples/example_usage.py
```

## What the Example Does

The example script demonstrates:
1. Initializing the Research Assistant
2. Ingesting web pages from Wikipedia
3. Researching a topic with citation-aware summaries
4. Managing the knowledge base

## Creating Your Own Examples

You can use this template to create your own research workflows:

```python
from research_assistant.assistant import ResearchAssistant

# Initialize
assistant = ResearchAssistant()

# Ingest sources
assistant.ingest_sources([
    "https://example.com/article1",
    "https://example.com/article2",
    "path/to/document.pdf"
])

# Research a topic
brief = assistant.research("Your research question")
print(brief.format())
```
