import requests
import os
from datetime import datetime, date
from polylog import setup_logger
from typing import Union

# Initialize logger
logger = setup_logger(__name__)

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
    WL_API_KEY: Union[None, str] = os.getenv("WARCRAFT_LOGS_API_KEY")

    # Base URL for Warcraft logs API
    base_guild_url: str = (
        BASE_REQUEST_URL + "reports/guild/Casual%20Progress/eredar/eu?api_key="
    )

    # Fetch API key from environment variables
    url: str = base_guild_url + str(WL_API_KEY)
    data: requests.Response = requests.get(url)
    try:
        if data.status_code == 200:
            # Parse the response JSON
            data_json: dict = data.json()
            # Fetch log ID
            logs_id: str = data_json[0]["id"]

            # Construct the log URL
            response: str = BASE_RESPONSE_REPORTS_URL + logs_id

            return response

        else:
            logger.warning(
                f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m"
            )
            return "> **ERROR: Something went wrong, please try again later!**"

    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"


async def logs_from(date: date) -> str:
    """Fetches the Warcraft logs for a particular date and returns the log URLs.

    Args:
        date (date): The date to fetch the logs for.

    Returns:
        str: URLs of the logs or an error message.
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
    urls = []
    try:
        if data.status_code == 200:
            # Parse the response JSON
            data_json = data.json()

            for log in data_json:
                # Fetch log ID
                log_id = log["id"]

                # Fetch log start timestamp
                start_timestamp = log["start"]
                start_datetime = datetime.fromtimestamp(start_timestamp / 1000)

                # Check if the date matches
                if start_datetime.date() == date:
                    # Construct the log URL
                    log_url = BASE_RESPONSE_REPORTS_URL + log_id
                    urls.append(log_url)

            return "\n".join(urls) if urls else "> **ERROR: No logs found for the given date!**"

        else:
            logger.warning(
                f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m"
            )
            return "> **ERROR: Something went wrong, please try again later!**"

    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"

