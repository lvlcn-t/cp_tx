import requests
from src import log
import os

logger = log.setup_logger(__name__)




async def response_latest(client) -> str:

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
