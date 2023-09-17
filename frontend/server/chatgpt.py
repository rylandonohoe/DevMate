import os
import sys
import server.constants as constants
import langchain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.storage import InMemoryStore, LocalFileStore, RedisStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings

os.environ["OPENAI_API_KEY"] = constants.APIKEY

def initialize_embeddings():
    fs = LocalFileStore("./test_cache/")

    underlying_embeddings = OpenAIEmbeddings()

    embedder2 = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, fs, namespace=underlying_embeddings.model)

    loader = DirectoryLoader("data", silent_errors=True, loader_cls=TextLoader)
    index = VectorstoreIndexCreator(embedding=underlying_embeddings).from_loaders([loader])

def askQuery(question):
    
    response = index.query(question, llm=ChatOpenAI())
    return response

#initialize_embeddings()

"""
    # Initialize Langchain
    underlying_embeddings = OpenAIEmbeddings()

    fs = LocalFileStore("./cache/")

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(underlying_embeddings, fs, namespace=underlying_embeddings.model)


    store = InMemoryStore()
    fs = LocalFileStore("./cache/")

loader = DirectoryLoader("data", silent_errors=True, loader_cls=TextLoader)


while True:
    query = input("Enter your query: ")

    # Check if the embedding is in the cache, if not, compute and cache it
    if query not in embedding_cache:
        
        embeddings = index.query(query, llm=ChatOpenAI())
        
        # Store the computed embedding in the cache
        embedding_cache[query] = embeddings

    # Retrieve the embedding from the cache
    cached_embedding = embedding_cache.get(query, None)

    if cached_embedding:
        print("Cached Embedding:")
        print(cached_embedding)
    else:
        print("Embedding not found in cache. Something went wrong during computation.")

"""