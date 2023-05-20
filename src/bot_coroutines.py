from src import warcraftlogs, log, responses
import asyncio
from datetime import datetime

# Initialize logger
logger = log.setup_logger(__name__)

previous_embed = None


async def fetch_function_data(callback_function):
        """
        An async function to fetch a functions response.

        Args:
            callback_function (function): The function to call to get the data.

        Returns:
            data: The data returned by the callback_function.
        """
        data = await callback_function()
        return data

async def startLogs(client, interaction, response=None):
    """
    This function is used to check for updates on a website. It's an asyncio coroutine and should be used with await.

    Args:
        client (discord.Client): The client object that will be used to send messages
        interaction (discord.Interaction): The interaction object that will be used to send messages
        response (str, optional): The previous content of the website. Defaults to None.

    Returns:
        None: This function does not return anything. It runs indefinitely.
    """
    # Updating global previous_content with the response, if provided
    global previous_embed
    previous_embed = response
    is_checking_logs = True
    
    async def check_website():
        """
        An async function that checks if the website content has changed.

        This function fetches the website content using fetch_website_content() and then checks if it has changed.
        If it has, it sends a message through the client and updates previous_content.
        """
        global previous_embed

        # Get the current date and time
        now = datetime.now()

        # Check if the current day is Tuesday or Friday, and the time is between 4 pm and 9 pm UTC (6 pm and 11 pm CEST)
        if (now.weekday() == 1 or now.weekday() == 4) and 16 <= now.hour < 21:
            try:
                content = await fetch_function_data(warcraftlogs.latest_logs)

                if content != previous_embed:
                    # Website content has changed
                    # Get the channel from the interaction's channel_id and send the message to the channel directly
                    channel = client.get_channel(interaction.channel_id)
                    await channel.send(content)
                    previous_embed = content
                    logger.info("Website content has been updated.")
                else:
                    logger.info("Website content has not changed.")
            except Exception as e:
                logger.error(f"An error occurred in check_website: {e}")
        else:
            logger.info("Not the right time for checking the website content.")

    while is_checking_logs:
        try:
            await check_website()
            await asyncio.sleep(120)  # Wait for 2 minutes
        except Exception as e:
            logger.error(f"An error occurred in check_update: {e}")
            
async def stopLogs():
    global is_checking_logs
    is_checking_logs = False

async def checkGuildKills(client, interaction, embed=None):
    """
    This function is used to check for updates on a website. It's an asyncio coroutine and should be used with await.

    Args:
        client (discord.Client): The client object that will be used to send messages
        interaction (discord.Interaction): The interaction object that will be used to send messages
        response (str, optional): The previous content of the website. Defaults to None.

    Returns:
        None: This function does not return anything. It runs indefinitely.
    """
    # Updating global previous_content with the response, if provided
    global previous_embed
    previous_embed = embed

    # Instead of using the interaction response, send a regular message and keep a reference to it
    message = await client.send_message(interaction, previous_embed)
    
    async def check_guild_embed():
        """
        An async function that checks if the guild's rio data has changed.

        This function fetches the website content using fetch_website_content() and then checks if it has changed.
        If it has, it sends a message through the client and updates previous_content.
        """
        global previous_embed

        try:
            content = await fetch_function_data(responses.prepare_rio_guild_embed)

            if content != previous_embed:
                # Edit the message directly
                await message.edit(embed=content)
                previous_embed = content
                logger.info("Guild embed has been updated.")
            else:
                logger.info("Guild embed has not changed.")
        except Exception as e:
            logger.error(f"An error occurred in check_website: {e}")

    while True:
        try:
            await check_guild_embed()
            await asyncio.sleep(3600)  # Wait for 1 hour
        except Exception as e:
            logger.error(f"An error occurred in check_update: {e}")