import os
import sys
import constants
import langchain
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.storage import InMemoryStore, LocalFileStore, RedisStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.llms import OpenAI
from langchain.memory import ConversationEntityMemory
from langchain.memory import ConversationBufferMemory

from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Define a cache to store embeddings
embedding_cache = {}

# Initialize Langchain
underlying_embeddings = OpenAIEmbeddings()
store = InMemoryStore()
fs = LocalFileStore("./cache/")

loader = DirectoryLoader("data", silent_errors=True, loader_cls=TextLoader)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
index = VectorstoreIndexCreator().from_loaders([loader])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

while True:
    qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0, model="gpt-3.5-turbo"), vectorstore.as_retriever(), memory=memory)
    query = input("Enter your query: ")
    result = qa({"question": query})

    print(result["answer"])

    # Check if the embedding is in the cache, if not, compute and cache it
   # if query not in embedding_cache:
        
      #  embeddings = index.query(query, llm=ChatOpenAI())
        
        
        # Store the computed embedding in the cache
     #   embedding_cache[query] = embeddings

    # Retrieve the embedding from the cache
  #  cached_embedding = embedding_cache.get(query, None)
  #  result = qa({"question": query})
   # print(result["answer"])

    
