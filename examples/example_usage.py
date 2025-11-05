"""Example usage of the Research Assistant."""

import os
from pathlib import Path

# Set up environment (for demo purposes - normally use .env file)
if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY environment variable not set")
    print("Please set your OpenAI API key:")
    print("  export OPENAI_API_KEY='your-api-key-here'")
    exit(1)

from research_assistant.assistant import ResearchAssistant

def main():
    """Demonstrate the Research Assistant capabilities."""
    
    print("=" * 80)
    print("Research Assistant Demo")
    print("=" * 80)
    print()
    
    # Initialize the assistant
    print("Initializing Research Assistant...")
    assistant = ResearchAssistant()
    print("✓ Assistant initialized")
    print()
    
    # Example 1: Ingest web pages
    print("-" * 80)
    print("Example 1: Ingesting web pages")
    print("-" * 80)
    
    sources = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning"
    ]
    
    print(f"Ingesting {len(sources)} web pages...")
    for source in sources:
        print(f"  - {source}")
    
    try:
        assistant.ingest_sources(sources)
        print("✓ Successfully ingested sources")
    except Exception as e:
        print(f"✗ Error ingesting sources: {str(e)}")
        print("Note: This requires internet access")
    
    print()
    
    # Example 2: Research a topic
    print("-" * 80)
    print("Example 2: Researching a topic")
    print("-" * 80)
    
    query = "What is the difference between artificial intelligence and machine learning?"
    print(f"Query: {query}")
    print()
    
    try:
        brief = assistant.research(query)
        print(brief.format())
    except Exception as e:
        print(f"✗ Error during research: {str(e)}")
    
    print()
    
    # Example 3: Clear knowledge base
    print("-" * 80)
    print("Example 3: Managing knowledge base")
    print("-" * 80)
    
    print("To clear the knowledge base:")
    print("  assistant.clear_knowledge_base()")
    print()
    
    print("=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Try the CLI: research-assistant --help")
    print("  2. Ingest your own sources: research-assistant ingest <url-or-pdf>")
    print("  3. Research topics: research-assistant research 'your query'")
    print()


if __name__ == "__main__":
    main()
