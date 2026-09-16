"""Recommended project layout:

my_ai_project/
src/
my_ai_project/
__init__.py
config.py ← LLMConfig and settings
clients/
__init__.py
anthropic.py ← AnthropicClient
openai.py ← OpenAIClient
retrieval/
__init__.py
chunker.py ← chunk_text generator
embedder.py ← embed_texts function
pipeline.py ← main RAG pipeline
tests/
test_config.py
test_chunker.py
pyproject.toml
README.md
"""