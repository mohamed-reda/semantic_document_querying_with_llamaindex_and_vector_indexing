from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

from common_llm_models import setup_models


def load_data(directory):
    """Load data from the specified directory."""
    return SimpleDirectoryReader(directory).load_data()


def initialize_chroma_db(path, collection_name):
    """Initialize ChromaDB client and create/get a collection."""

    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context, chroma_collection


def create_or_load_index(documents, storage_context):
    """Create or load an index based on whether the Chroma collection contains data."""
    # Check if the 'chroma_db' folder exists
    item_count = storage_context.vector_store._collection.count()
    if item_count > 0:
        print(f"Indexed data found with {item_count} items. Loading existing index...")
        return VectorStoreIndex.from_vector_store(
            storage_context.vector_store, storage_context=storage_context, show_progress=True
        )
    else:
        print("No indexed data found in Chroma collection. Creating new index...")
        # Create a new index
        return VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )


def setup_query_engine(index):
    """Set up the query engine with retriever and response synthesizer."""
    retriever = VectorIndexRetriever(index=index, similarity_top_k=20)
    response_synthesizer = get_response_synthesizer()
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.4)],
    )
    return query_engine


def main():
    # Setup models
    setup_models()

    # Load data
    documents = load_data("../data/paul_graham/")
    print(f"Number of documents loaded: {len(documents)}")

    # Initialize ChromaDB
    storage_context, chroma_collection = initialize_chroma_db("./chroma_db", "quickstart")
    print(f"Number of items in Chroma collection: {chroma_collection.count()}")

    # Create or load index
    index = create_or_load_index(documents, storage_context)

    # Set up query engine
    query_engine = setup_query_engine(index)

    # Query
    response = query_engine.query("What did Paul Graham learn from his painting experience?")
    print("***********")
    print(response)
    print("***********")


if __name__ == "__main__":
    main()

"""
Project name is :1 Document Query Engine with chromadb

For first time:

Number of documents loaded: 1
Number of items in Chroma collection: 0
No indexed data found in Chroma collection. Creating new index...
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00, 15.16it/s]
Generating embeddings: 100%|██████████| 621/621 [05:20<00:00,  1.94it/s]
***********
Paul Graham realized that painting could be a lasting form of art that doesn't fade over time. He discovered his ability to create unique, identifiable styles in his paintings, distinguishing them from others'. Through his practice, he appreciated the value in paying close attention to details and capturing realistic still life scenes. This process allowed him to observe subjects meticulously and uncover new insights even after extended periods of focused work.
***********


For second time it gets:
Number of documents loaded: 1
Number of items in Chroma collection: 621
Indexed data found with 621 items. Loading existing index...
***********
Paul Graham learned about the process of creating a distinctive signature style in his paintings at RISD. He realized that painting requires focusing on detailed elements to make something unique and lasting, rather than just copying still lifes or portraits quickly. Graham noticed how students were encouraged to express themselves uniquely, unlike when looking at everyday scenes where brains handle low-level visual processes without conscious attention to fine details.
***********


"""
