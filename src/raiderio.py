import requests
from src import log
import os
import json

# Initialize the logger.
logger = log.setup_logger(__name__)

BASE_URL = "https://raider.io/"
BASE_REQUEST_URL = BASE_URL + "api/v1/"

EXPANSION_ID = 9  # ! This must be updated when a new expansion is released.

async def guild_profile():
    """
    Asynchronously fetches guild profile information from Raider.io API.
    
    Returns:
        tuple: Contains raid progression information, boss names and latest boss kill links.
    """
    try:
        # Define the url for the guild profile API endpoint.
        url = BASE_REQUEST_URL + "guilds/profile?region=eu&realm=eredar&name=casual%20progress&fields=raid_progression"
        raid_progression = getRIOData(url)

        url = BASE_REQUEST_URL + "raiding/static-data?expansion_id=" + str(EXPANSION_ID)
        static_raiding_data = getRIOData(url)

        difficulty = None
        boss_names = []
        latest_boss_kills = []
        for index, raid in enumerate(raid_progression["raid_progression"].values()): # type: ignore
            boss_id = (int(raid["summary"][0]) - 1)
            if "N" in raid["summary"]:
                difficulty = "normal"
            elif "H" in raid["summary"]:
                difficulty = "heroic"
            elif "M" in raid["summary"]:
                difficulty = "mythic"
            else:
                raise Exception("Error in retrieving the boss_id or raid difficulty")

            # Generate the URL for the latest boss kill.
            latest_boss_kills.append(
                BASE_URL
                + "guilds/eu/eredar/Casual%20Progress/raid-encounters/"
                + difficulty
                + "/"
                + static_raiding_data["raids"][index]["slug"] # type: ignore
                + "/"
                + (
                    static_raiding_data["raids"][index]["encounters"][ # type: ignore
                        boss_id
                    ]["slug"]
                )
            )

            # Append boss name.
            boss_names.append(static_raiding_data["raids"][index]["encounters"][boss_id]["name"]) # type: ignore
        
        return raid_progression, boss_names, latest_boss_kills
    
    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"


async def character_profile() -> str:
    pass
    return str()


def getRIOData(url):
    """
    Fetches data from the Raider.io API for a given URL.
    
    Args:
        url (str): The url for the Raider.io API endpoint.
        
    Returns:
        dict: The json response from the API parsed as a dict.
        str: Error message if an exception occurs.
    """
    try:
        data = requests.get(url)
        if data.status_code == 200:
            # Parse the data JSON as dict.
            return json.loads(data.text)
        else:
            logger.warning(
                f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m"
            )
            return "> **ERROR: Something went wrong, please try again later!**"

    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"
