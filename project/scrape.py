# combine all information into one directory 
import requests
import constants

# Replace these variables with your GitHub username, repository, and access token

access_token = constants.GITKEY
username = constants.GITUSERNAME

# Create a session with your access token
session = requests.Session()
session.auth = (username, access_token)

# Define the API URL for issues
api_url = f"https://api.github.com/repos/Shared-Reality-Lab/IMAGE-server/issues"
output_file = "github_issues.txt"
file = open(output_file, "w")

try:
    # Send a GET request to the GitHub API
    response = session.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        issues = response.json()
        
        # Loop through the issues and print their titles
        for issue in issues:
            file.write(f"Issue #{issue['number']}: {issue['title']}  ")
            if (issue['assignee']):
                file.write(f"Assigned to: {issue['assignee']['login']}")
            comments_url = issue['comments_url']
            
            # Send a GET request to the comments URL
            comments_response = session.get(comments_url)

            # Check if the request for comments was successful (status code 200)
            if comments_response.status_code == 200:
                comments = comments_response.json()
                
                # Loop through the comments and print the author and body
                for comment in comments:
                    file.write(f"Comment by {comment['user']['login']} on issue #{issue['number']}:\n  {comment['body']}\n")

    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
