"""Command-line interface for Research Assistant."""

import click
import logging
import sys
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler

from .assistant import ResearchAssistant
from .config import get_config

# Set up rich console
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)

logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug):
    """Research Assistant with RAG & Citation-Aware Summaries."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command()
@click.argument('sources', nargs=-1, required=True)
def ingest(sources):
    """
    Ingest documents from URLs or PDF files.
    
    Examples:
        research-assistant ingest https://example.com/article
        research-assistant ingest document.pdf
        research-assistant ingest https://site.com doc1.pdf doc2.pdf
    """
    try:
        console.print("[bold blue]Starting document ingestion...[/bold blue]")
        
        assistant = ResearchAssistant()
        assistant.ingest_sources(list(sources))
        
        console.print(f"[bold green]✓ Successfully ingested {len(sources)} source(s)[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--num-sources', '-n', type=int, help='Number of sources to use')
@click.option('--output', '-o', type=click.Path(), help='Save output to file')
def research(query, num_sources, output):
    """
    Research a topic and generate a citation-aware summary.
    
    Examples:
        research-assistant research "What are the benefits of AI?"
        research-assistant research "Climate change impacts" -n 10
        research-assistant research "Machine learning" -o report.txt
    """
    try:
        console.print(f"[bold blue]Researching: {query}[/bold blue]")
        console.print()
        
        assistant = ResearchAssistant()
        brief = assistant.research(query, num_sources=num_sources)
        
        # Format and display
        formatted_output = brief.format()
        console.print(formatted_output)
        
        # Save to file if requested
        if output:
            Path(output).write_text(formatted_output)
            console.print()
            console.print(f"[bold green]✓ Saved to {output}[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
def clear():
    """Clear all ingested documents from the knowledge base."""
    try:
        if click.confirm('Are you sure you want to clear all documents?'):
            console.print("[bold yellow]Clearing knowledge base...[/bold yellow]")
            
            assistant = ResearchAssistant()
            assistant.clear_knowledge_base()
            
            console.print("[bold green]✓ Knowledge base cleared[/bold green]")
        else:
            console.print("Cancelled")
            
    except Exception as e:
        console.print(f"[bold red]✗ Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
def info():
    """Display configuration information."""
    try:
        config = get_config()
        
        console.print("[bold]Research Assistant Configuration[/bold]")
        console.print()
        console.print(f"OpenAI Model: {config.openai_model}")
        console.print(f"Embedding Model: {config.embedding_model}")
        console.print(f"ChromaDB Path: {config.chroma_db_path}")
        console.print(f"Collection Name: {config.collection_name}")
        console.print(f"Chunk Size: {config.chunk_size}")
        console.print(f"Chunk Overlap: {config.chunk_overlap}")
        console.print(f"Top K Results: {config.top_k_results}")
        console.print(f"Temperature: {config.temperature}")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {str(e)}[/bold red]")
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
