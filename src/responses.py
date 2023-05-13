import requests
from src import log
import os
from github import Github

logger = log.setup_logger(__name__)

async def latest_wc_logs(client) -> str:

    base_url='https://www.warcraftlogs.com:443/v1/reports/guild/Casual%20Progress/eredar/eu?api_key='
    base_response="https://www.warcraftlogs.com/reports/"

    WL_API_KEY=os.getenv("WARCRAFT_LOGS_API_KEY")
    url = base_url + str(WL_API_KEY)
    data = requests.get(url)
    try:
        if data.status_code == 200:
            data_json = data.json()
            logs_id = data_json[0]['id']

            response = base_response + logs_id
            
            return response
            
        else:
            logger.warning(f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m")
            return "> **ERROR: Something went wrong, please try again later!**"
        
    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"

async def create_github_issue(title: str, body: str, labels: list):
    try:
        repo = get_repo("lvlcn-t/cp_tx")
        issue = repo.create_issue(title=title, body=body, labels=labels)
        return issue.number
    except Exception as e:
        logger.exception(f"Error while creating GitHub issue: {e}")
        return None

def get_repo(repo_name):
    GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)

    return repo
