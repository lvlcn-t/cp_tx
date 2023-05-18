import requests
from src import log
import os
import json

# Initialize logger
logger = log.setup_logger(__name__)

BASE_URL = "https://raider.io/"
BASE_REQUEST_URL = BASE_URL + "api/v1/"
EXPANSION_ID = 9

async def guild_profile():
    try:
        url = BASE_REQUEST_URL + "guilds/profile?region=eu&realm=eredar&name=casual%20progress&fields=raid_progression"
        raid_progression = getRIOData(url)
        difficulty = None
        boss_id = int(raid_progression["raid_progression"].values()[0]["summary"][0]) - 1
        if "N" in raid_progression["raid_progression"].values()[0]["summary"]:
            difficulty = "normal"
        elif "H" in raid_progression["raid_progression"].values()[0]["summary"]:
            difficulty = "heroic"
        elif "M" in raid_progression["raid_progression"].values()[0]["summary"]:
            difficulty = "mythic"
        else:
            return "> **ERROR: Something went wrong, please try again later!**"

        url = BASE_REQUEST_URL + "raiding/static-data?expansion_id=" + str(EXPANSION_ID)
        static_raiding_data = getRIOData(url)

        url = BASE_REQUEST_URL + "guilds/boss-kill?region=eu&realm=eredar&\
            guild=casual%20progress&raid=" + static_raiding_data["raids"][0]["slug"] + "&\
            boss=" + static_raiding_data["raids"][0]["encounters"][boss_id]["slug"] + "&difficulty=" + difficulty
        latest_boss_kill = getRIOData(url)
    
    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"
    

async def character_profile() -> str:
    pass
    return str()

def getRIOData(url):
    try:
        data = requests.get(url)
        if data.status_code == 200:
            # Parse the data JSON as dict
            return(json.loads(data.text))
        else:
            logger.warning(f"\x1b[31mRequest failed with status code {data.status_code}\x1b[0m")
            return "> **ERROR: Something went wrong, please try again later!**"
        
    except Exception as e:
        logger.exception(f"Error while sending message: {e}")
        return "> **ERROR: Something went wrong, please try again later!**"