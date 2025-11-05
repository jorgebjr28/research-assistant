"""Command-line interface for the Research Assistant."""

import argparse
import sys
from typing import List
from .rag_pipeline import RAGPipeline
from .vector_store import VectorStore


def ingest_command(args):
    """Handle the ingest command."""
    print(f"Ingesting {len(args.sources)} source(s)...")
    
    pipeline = RAGPipeline()
    result = pipeline.ingest_sources(args.sources)
    
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"  Sources ingested:")
        for source in result['sources']:
            print(f"  - {source}")
    else:
        print(f"✗ {result['message']}")
        sys.exit(1)


def query_command(args):
    """Handle the query command."""
    print(f"Researching topic: {args.topic}")
    print("-" * 60)
    
    pipeline = RAGPipeline()
    brief = pipeline.synthesize_research_brief(args.topic, args.num_sources)
    
    print(brief['summary'])
    
    if args.show_excerpts and brief['excerpts']:
        print("\n## Detailed Excerpts\n")
        for excerpt in brief['excerpts']:
            print(f"[{excerpt['citation_index']}] {excerpt['text']}")
            print()


def stats_command(args):
    """Handle the stats command."""
    pipeline = RAGPipeline()
    stats = pipeline.get_stats()
    
    print("Vector Store Statistics:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Persist directory: {stats['persist_directory']}")


def clear_command(args):
    """Handle the clear command."""
    if not args.force:
        response = input("Are you sure you want to clear the vector store? (yes/no): ")
        if response.lower() != 'yes':
            print("Clear operation cancelled.")
            return
    
    vector_store = VectorStore()
    vector_store.clear()
    print("✓ Vector store cleared successfully.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Research Assistant with RAG & Citation-Aware Summaries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest documents from URLs
  %(prog)s ingest https://example.com/article1.html https://example.com/article2.pdf
  
  # Query on a topic
  %(prog)s query "machine learning applications" --num-sources 5
  
  # Show statistics
  %(prog)s stats
  
  # Clear the vector store
  %(prog)s clear --force
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ingest command
    ingest_parser = subparsers.add_parser(
        'ingest',
        help='Ingest documents from URLs or file paths into the vector store'
    )
    ingest_parser.add_argument(
        'sources',
        nargs='+',
        help='URLs or file paths to ingest'
    )
    ingest_parser.set_defaults(func=ingest_command)
    
    # Query command
    query_parser = subparsers.add_parser(
        'query',
        help='Query the research assistant on a topic'
    )
    query_parser.add_argument(
        'topic',
        help='Topic or question to research'
    )
    query_parser.add_argument(
        '--num-sources',
        type=int,
        default=5,
        help='Number of sources to retrieve (default: 5)'
    )
    query_parser.add_argument(
        '--show-excerpts',
        action='store_true',
        help='Show detailed excerpts from sources'
    )
    query_parser.set_defaults(func=query_command)
    
    # Stats command
    stats_parser = subparsers.add_parser(
        'stats',
        help='Show vector store statistics'
    )
    stats_parser.set_defaults(func=stats_command)
    
    # Clear command
    clear_parser = subparsers.add_parser(
        'clear',
        help='Clear all documents from the vector store'
    )
    clear_parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )
    clear_parser.set_defaults(func=clear_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()
