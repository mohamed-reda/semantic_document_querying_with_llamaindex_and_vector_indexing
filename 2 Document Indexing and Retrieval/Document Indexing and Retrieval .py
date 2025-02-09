import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

from common_llm_models import setup_models

setup_models()

# --------
documents = SimpleDirectoryReader("../pdf/").load_data()

if os.path.exists("storage"):
    print("Loading index from storage")
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(storage_context)
else:
    print("Creating new index")
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="storage")

query_engine = index.as_query_engine()

response = query_engine.query("What are the design goals and give details about it please.")
print(response)

"""

Project name is : 2 Document Indexing and Retrieval

output:

AUTO GEN STUDIO is designed to enhance the MULTI -AGENT developer experience by focusing on three core objectives:

1. **Rapid Prototyping**: This goal aims to provide a platform where developers can quickly specify agent configurations and compose these agents into effective multi-agent workflows.

2. **Developer Tooling**: The tooling offered supports understanding and debugging of agent behaviors, which helps in improving multi-agent systems.

3. **Reusable Templates**: AUTO GEN STUDIO provides a gallery of reusable, shareable templates to help bootstrap the creation of agent workflow. This approach aims to establish shared standards and best practices for MULTI -AGENT system development, thereby promoting wider adoption and implementation of MULTI -AGENT solutions.
"""
