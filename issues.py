import requests
import constants
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


# Replace these variables with your GitHub username, repository, and access token

access_token = constants.GITKEY
username = constants.GITUSERNAME


def createIssue(title, body):
    api_url = f"https://api.github.com/repos/rianadutta/IMAGE-server/issues"
    payload = {
    'title': title,
    'body': body
    }

    # Create the issue using the GitHub API
    headers = {
        'Authorization': f'token {access_token}'
    }

    response = requests.post(api_url, json=payload, headers=headers)

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)


def addComment(description, solution):
    api_url = f"https://api.github.com/repos/rianadutta/IMAGE-server/issues"
    session = requests.Session()
    session.auth = (username, access_token)
    response = session.get(api_url)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            problem = issue['title']
            
        

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([preprocess_text(description), preprocess_text(problem)])

            cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
           
          

            # Define a threshold for similarity
            similarity_threshold = 0.5

            if cosine_sim >= similarity_threshold:
                issue_number = issue['number']
                comments_url = f'https://api.github.com/repos/rianadutta/IMAGE-server/issues/{issue_number}/comments'
                payload = {
                    'body': f'Automated message from DevMate: Hi! I might have found a solution for your problem. {solution}'
                }
                headers = {
                    'Authorization': f'token {access_token}'
                }
                response = requests.post(comments_url, json=payload, headers=headers)

               
            
             

addComment("cannot update preprocessor names", "update name through ssh")

