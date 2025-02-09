from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.chat_engine.types import ChatMode

from common_llm_models import setup_models

setup_models()

data = SimpleDirectoryReader(input_dir="../data/paul_graham/", ).load_data()
index = VectorStoreIndex.from_documents(data, show_progress=True)

chat_engine = index.as_chat_engine(chat_mode=ChatMode(value='condense_question'), verbose=True)
# response = chat_engine.chat("What did Paul Graham do after YC?")

while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = chat_engine.chat(text_input)
    print(f"Agent: {response}")

"""
Project name is :4 full Conversational Chatbot in cmd with the data
"""
