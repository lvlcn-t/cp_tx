from src import log
import os
from github import Github

# Initialize logger
logger = log.setup_logger(__name__)


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


def validate_response(response):
    """Validates a response to ensure it follows a specific format.

    This function checks that a response has a title line that isn't empty, and a second line consisting of '---'.

    Args:
        response (str): The response to validate.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    lines = response.split("\n")

    # Check if the 'title' line exists and is not empty
    title_exists = any(
        line.strip().lower().startswith("title:") and line.strip().lower() != "title:"
        for line in lines
    )

    # Check if the second '---' line exists
    second_dash_line_exists = "---" in lines[1:]

    return title_exists and second_dash_line_exists


# Function to clean the template by removing specific lines
def clean_template(template: str, lines_to_remove: list):
    """Removes specified lines from a given template.

    Args:
        template (str): The original template.
        lines_to_remove (list): The lines that need to be removed out of the template.

    Returns:
        str: The template with the provided lines removed.
    """

    for line in lines_to_remove:
        template = template.replace(line, "")

    return template


# Function to extract relevant information from a user's response
def get_response_info(response, author_name, author_discriminator=None):
    """Extracts the title and body from a user's response.

    Args:
        response (discord.Message): User's response to the bot's request.
        author_name (str): The username of the author.
        author_discriminator (str, optional): The discriminator of the author. Defaults to None.

    Returns:
        tuple: Contains the title (str) and body (str) of the user's response.
    """

    # Extract information from the user's response
    lines = response.content.split("\n")
    title = None
    body = ""
    is_body = False
    for line in lines:
        # Use lower() to make the check case-insensitive
        if line.lower().startswith("title:"):
            title = line.replace("title:", "").strip()
            title = title.replace("'", "")
        elif line.strip() == "---" and not is_body:
            is_body = True
        elif is_body and not line.strip() == "---":
            body += line + "\n"

    if author_discriminator is not None:
        body += f"\n\n**From: {author_name}#{author_discriminator}**"
    else:
        body += f"\n\n**From: @{author_name}**"

    return title, body
