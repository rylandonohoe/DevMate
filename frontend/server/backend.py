import re
from datetime import datetime
from g4f import ChatCompletion
from flask import request, Response, stream_with_context
from requests import get
from server.config import special_instructions
import server.chatgpt as chatgpt
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.vectorstores import Chroma
import server.issues as issues


db = None
history = []
response = ""
messages = None

class Backend_Api:

    def __init__(self, bp, config: dict) -> None:
        global db

        """
        Initialize the Backend_Api class.
        :param app: Flask application instance
        :param config: Configuration dictionary
        """
        self.bp = bp
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            },
            '/processIssue': {
                'function': self._addCommentToIssue,
                'methods': ['POST']
            },
            '/addIssue': {
                'function': self._addNewIssue,
                'methods': ['POST']
            }
        }
        raw_documents = DirectoryLoader('./server/data').load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        db = Chroma.from_documents(documents, OpenAIEmbeddings())

    def _addCommentToIssue(self):
        global history
        issues.addComment(messages[0]['content'], response)
        print("added comment" + messages[0]['content'] + response)
        history = []
        return "ok"
    
    def _addNewIssue(self):
        global history
        prompt = "Summarize the following in 10 words or less: " + messages[0]['content']
        summary = ChatCompletion.create(
            messages= prompt,
            model="gpt-3.5-turbo",
            temperature=0,
        )
        issues.createIssue(summary, messages[0]['content'])
        print("Issue created" + summary + messages[0]['content'])
        history = []
        return "ok"
    
    def _conversation(self):
        global history
        global issueResolved
        global issueNeverResolved
        global response
        global messages

        """  
        Handles the conversation route.  

        :return: Response object containing the generated conversation stream  
        """
        conversation_id = request.json['conversation_id']

        try:
            
            jailbreak = request.json['jailbreak']
            model = request.json['model']
            messages = build_messages(jailbreak)

            # Generate response
            qu = messages[len(messages) - 1]['content']
            docs = db.similarity_search(qu)
            content = docs[0].page_content

            query = f"""Use the collection of data from IMAGE as a reference but don't EVER tell the user you know about the IMAGEData. IMAGE is a research project at McGill University. The IMAGEData contains the GitHub wiki, the issues and source code. 
            IMAGEData:
            \"\"\"
            {content}
            \"\"\"
            Question: {qu}"""

            history.append({'role': 'system', 'content': 'You answer questions about the IMAGE project.'})
            history.append({'role': 'user', 'content': query})

            response = ChatCompletion.create(
            messages=history,
            model="gpt-3.5-turbo",
            temperature=0,
            )


            return Response(stream_with_context(generate_stream(response, jailbreak)), mimetype='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)

            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, 400


def build_messages(jailbreak):
    """  
    Build the messages for the conversation.  

    :param jailbreak: Jailbreak instruction string  
    :return: List of messages for the conversation  
    """
    _conversation = request.json['meta']['content']['conversation']
    internet_access = request.json['meta']['content']['internet_access']
    prompt = request.json['meta']['content']['parts'][0]

    # Add the existing conversation
    conversation = _conversation

    # Add web results if enabled
    if internet_access:
        current_date = datetime.now().strftime("%Y-%m-%d")
        query = f'Current date: {current_date}. ' + prompt["content"]
        search_results = fetch_search_results(query)
        conversation.extend(search_results)

    # Add jailbreak instructions if enabled
    if jailbreak_instructions := getJailbreak(jailbreak):
        conversation.extend(jailbreak_instructions)

    # Add the prompt
    conversation.append(prompt)

    # Reduce conversation size to avoid API Token quantity error
    if len(conversation) > 3:
        conversation = conversation[-4:]

    return conversation


def fetch_search_results(query):
    """  
    Fetch search results for a given query.  

    :param query: Search query string  
    :return: List of search results  
    """
    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 3,
                 })

    snippets = ""
    for index, result in enumerate(search.json()):
        snippet = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
        snippets += snippet

    response = "Here are some updated web searches. Use this to improve user response:"
    response += snippets

    return [{'role': 'system', 'content': response}]


def generate_stream(response, jailbreak):
    """
    Generate the conversation stream.

    :param response: Response object from ChatCompletion.create
    :param jailbreak: Jailbreak instruction string
    :return: Generator object yielding messages in the conversation
    """
    if getJailbreak(jailbreak):
        response_jailbreak = ''
        jailbroken_checked = False
        for message in response:
            response_jailbreak += message
            if jailbroken_checked:
                yield message
            else:
                if response_jailbroken_success(response_jailbreak):
                    jailbroken_checked = True
                if response_jailbroken_failed(response_jailbreak):
                    yield response_jailbreak
                    jailbroken_checked = True
    else:
        yield from response


def response_jailbroken_success(response: str) -> bool:
    """Check if the response has been jailbroken.

    :param response: Response string
    :return: Boolean indicating if the response has been jailbroken
    """
    act_match = re.search(r'ACT:', response, flags=re.DOTALL)
    return bool(act_match)


def response_jailbroken_failed(response):
    """
    Check if the response has not been jailbroken.

    :param response: Response string
    :return: Boolean indicating if the response has not been jailbroken
    """
    return False if len(response) < 4 else not (response.startswith("GPT:") or response.startswith("ACT:"))


def getJailbreak(jailbreak):
    """  
    Check if jailbreak instructions are provided.  

    :param jailbreak: Jailbreak instruction string  
    :return: Jailbreak instructions if provided, otherwise None  
    """
    if jailbreak != "default":
        special_instructions[jailbreak][0]['content'] += special_instructions['two_responses_instruction']
        if jailbreak in special_instructions:
            special_instructions[jailbreak]
            return special_instructions[jailbreak]
        else:
            return None
    else:
        return None
