# Absolute imports - preferred
from my_ai_project.config import LLMConfig
from my_ai_project.clients.anthropic import AnthropicClient
# Import specific names
from my_ai_project.retrieval.chunker import chunk_text
# Import module as alias
import my_ai_project.retrieval.embedder as embedder
vectors = embedder.embed_texts(["hello", "world"])