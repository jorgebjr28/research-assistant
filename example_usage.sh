#!/bin/bash

# Example usage script for the Research Assistant
# This demonstrates the basic workflow of ingesting documents and querying

set -e

echo "=== Research Assistant Demo ==="
echo ""

# Use TF-IDF for offline environments
export USE_SENTENCE_TRANSFORMERS=false

# Step 1: Clear any existing database
echo "Step 1: Clearing existing database..."
python research_assistant.py clear --force
echo ""

# Step 2: Create example documents
echo "Step 2: Creating example documents..."
mkdir -p /tmp/demo_docs

cat > /tmp/demo_docs/python_basics.txt << 'EOF'
Python Programming Language

Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, as well as for use as a scripting or glue language to connect existing components together.

Python's simple, easy-to-learn syntax emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, which encourages program modularity and code reuse. The Python interpreter and the extensive standard library are available in source or binary form without charge for all major platforms and can be freely distributed.

Key Features:
- Easy to learn and use
- Interpreted language
- Object-oriented
- Large standard library
- Cross-platform compatibility
- Active community support

Popular applications include web development, data analysis, artificial intelligence, scientific computing, and automation.
EOF

cat > /tmp/demo_docs/data_science.txt << 'EOF'
Data Science Overview

Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. Data science is related to data mining, machine learning, and big data.

Data science is a "concept to unify statistics, data analysis, informatics, and their related methods" in order to "understand and analyze actual phenomena" with data. It uses techniques and theories drawn from many fields within the context of mathematics, statistics, computer science, information science, and domain knowledge.

Key Skills for Data Scientists:
- Statistics and mathematics
- Programming (Python, R, SQL)
- Machine learning algorithms
- Data visualization
- Domain expertise
- Communication skills

Applications of data science include predictive analytics, recommendation systems, fraud detection, customer segmentation, and natural language processing.
EOF

echo "Created demo documents in /tmp/demo_docs/"
echo ""

# Step 3: Ingest documents
echo "Step 3: Ingesting documents..."
python research_assistant.py ingest /tmp/demo_docs/python_basics.txt /tmp/demo_docs/data_science.txt
echo ""

# Step 4: Check statistics
echo "Step 4: Checking vector store statistics..."
python research_assistant.py stats
echo ""

# Step 5: Query on different topics
echo "Step 5: Querying on topic 'Python programming'..."
python research_assistant.py query "Python programming features" --num-sources 3
echo ""

echo "====================="
echo ""

echo "Step 6: Querying on topic 'data science'..."
python research_assistant.py query "What skills are needed for data science?" --num-sources 3 --show-excerpts
echo ""

echo "=== Demo Complete ==="
echo ""
echo "Try your own queries with:"
echo "  python research_assistant.py query \"your topic here\""
