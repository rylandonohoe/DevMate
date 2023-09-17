import requests
import constants

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




createIssue("read File", "cannot read file because of issue") 

