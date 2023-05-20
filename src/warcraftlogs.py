import requests
from src import log
import os
from datetime import datetime

# Initialize logger
logger = log.setup_logger(__name__)

# Set constants for base URLs
BASE_URL = "https://www.warcraftlogs.com"

BASE_REQUEST_URL = BASE_URL + ":443/v1/"

BASE_RESPONSE_URL = BASE_URL + "/"
BASE_RESPONSE_REPORTS_URL = BASE_RESPONSE_URL + "reports/"


async def latest_logs() -> str:
    """Fetches the latest Warcraft logs and returns the log URL.

    Returns:
        str: URL of the latest log or an error message
    """
    # Get WarcraftLogs API token from environment variables
    WL_API_KEY = os.getenv("WARCRAFT_LOGS_API_KEY")

    # Base URL for Warcraft logs API
    base_guild_url = (
        BASE_REQUEST_URL + "reports/guild/Casual%20Progress/eredar/eu?api_key="
    )

    # Fetch API key from environment variables
    url = base_guild_url + str(WL_API_KEY)
    data = requests.get(url)
    try:
        if data.status_code == 200:
            # Parse the response JSON
            data_json = data.json()
            # Fetch log ID
            logs_id = data_json[0]["id"]

            # Construct the log URL
            response = BASE_RESPONSE_REPORTS_URL + logs_id

            return response

        else:
            logger.warning(
                f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m"
            )
            return "> **ERROR: Something went wrong, please try again later!**"

    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"


async def logs(date: datetime) -> str:
    pass
    return str()
