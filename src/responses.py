import requests
from src import log
import os
from github import Github

# Initialize logger
logger = log.setup_logger(__name__)

async def latest_wc_logs() -> str:
    """Fetches the latest Warcraft logs and returns the log URL.

    Args:
        client: Discord client instance

    Returns:
        str: URL of the latest log or an error message
    """

    # Base URL for Warcraft logs API
    base_url='https://www.warcraftlogs.com:443/v1/reports/guild/Casual%20Progress/eredar/eu?api_key='
    # Base URL for the response link
    base_response="https://www.warcraftlogs.com/reports/"

    # Fetch API key from environment variables
    WL_API_KEY=os.getenv("WARCRAFT_LOGS_API_KEY")
    url = base_url + str(WL_API_KEY)
    data = requests.get(url)
    try:
        if data.status_code == 200:
            # Parse the response JSON
            data_json = data.json()
            # Fetch log ID
            logs_id = data_json[0]['id']

            # Construct the log URL
            response = base_response + logs_id
            
            return response
            
        else:
            logger.warning(f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m")
            return "> **ERROR: Something went wrong, please try again later!**"
        
    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"

async def create_github_issue(title: str, body: str, labels: list):
    """Creates a GitHub issue.

    Args:
        title (str): Title of the issue
        body (str): Body of the issue
        labels (list): List of labels to be added to the issue

    Returns:
        issue_number if successful or None if not
    """
    try:
        # Fetch the repository
        repo = get_repo("lvlcn-t/cp_tx")
        # Create the issue
        issue = repo.create_issue(title=title, body=body, labels=labels)
        return issue.number
    except Exception as e:
        logger.exception(f"Error while creating GitHub issue: {e}")
        return None

def get_repo(repo_name):
    """Fetches a GitHub repository.

    Args:
        repo_name (str): Full name of the repository (username/repo)

    Returns:
        Repository instance
    """
    
    # Get GitHub token from environment variables
    GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    # Instantiate a GitHub API instance
    g = Github(GITHUB_TOKEN)
    # Fetch the repository
    repo = g.get_repo(repo_name)

    return repo
