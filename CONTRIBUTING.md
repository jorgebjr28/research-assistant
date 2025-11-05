# Contributing to Research Assistant

Thank you for your interest in contributing to the Research Assistant project! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/jorgebjr28/research-assistant/issues) section
2. If not, create a new issue with:
   - A clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/jorgebjr28/research-assistant.git
   cd research-assistant
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Test CLI commands
   research-assistant --help
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes

## Development Setup

1. **Install in development mode**
   ```bash
   pip install -e .
   pip install pytest pytest-asyncio
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

## Testing Guidelines

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage
- Test both success and error cases

## Documentation

- Update README.md if you add new features
- Update QUICKSTART.md for user-facing changes
- Add docstrings to new functions and classes
- Include examples for new functionality

## Project Structure

```
research-assistant/
├── src/research_assistant/   # Main source code
│   ├── config.py             # Configuration
│   ├── ingestion.py          # Document ingestion
│   ├── vector_store.py       # Vector database
│   ├── rag_pipeline.py       # RAG implementation
│   ├── assistant.py          # Main interface
│   └── cli.py                # CLI commands
├── tests/                     # Test files
├── examples/                  # Example scripts
└── docs/                      # Documentation (future)
```

## Areas for Contribution

We welcome contributions in these areas:

- **New features**: Additional document types, improved RAG algorithms
- **Testing**: More comprehensive test coverage
- **Documentation**: Tutorials, examples, API documentation
- **Performance**: Optimization and caching improvements
- **UI/UX**: Better CLI output, web interface
- **Bug fixes**: Fix reported issues

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Clarification on contribution guidelines
- Discussion of new features

Thank you for contributing! 🎉
