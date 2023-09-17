import os
import sys
import constants
import langchain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.storage import InMemoryStore, LocalFileStore, RedisStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Define a cache to store embeddings
embedding_cache = {}

# Initialize Langchain
underlying_embeddings = OpenAIEmbeddings()
store = InMemoryStore()
fs = LocalFileStore("./cache/")

loader = DirectoryLoader("data", silent_errors=True, loader_cls=TextLoader)
index = VectorstoreIndexCreator().from_loaders([loader])

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
