from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.lmstudio import LMStudio


def setup_models():
    """Configure LLM and embedding models."""
    llm = LMStudio(
        model_name="qwen2.5-3b-instruct",
        base_url="http://localhost:11434/v1",
        temperature=0.6,
        request_timeout=190,
        # num_output=400,
    )
    embed_model = OpenAIEmbedding(
        api_base="http://localhost:11434/v1",
        model_name="text-embedding-nomic-embed-text-v1.5@f32"
    )
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 256
