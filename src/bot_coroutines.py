from src import warcraftlogs, responses
import asyncio
from datetime import datetime
from polylog import setup_logger

# Initialize logger
logger = setup_logger(__name__)

guild_previous_embed = None
logs_previous_content = None
is_checking_logs = None
is_checking_guild_profile = None

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
    global logs_previous_content
    logs_previous_content = response
    
    global is_checking_logs
    is_checking_logs = True
    logger.info("Log coroutine has been enabled.")
    
    async def check_website():
        """
        An async function that checks if the website content has changed.

        This function fetches the website content using fetch_website_content() and then checks if it has changed.
        If it has, it sends a message through the client and updates previous_content.
        """
        global logs_previous_content

        # Get the current date and time
        now = datetime.now()

        # Check if the current day is Tuesday or Friday, and the time is between 4 pm and 9 pm UTC (6 pm and 11 pm CEST)
        if (now.weekday() == 1 or now.weekday() == 4) and 16 <= now.hour < 21:
            try:
                content = await fetch_function_data(warcraftlogs.latest_logs)

                if content != logs_previous_content:
                    # Website content has changed
                    # Get the channel from the interaction's channel_id and send the message to the channel directly
                    channel = client.get_channel(interaction.channel_id)
                    await channel.send(content)
                    logs_previous_content = content
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
    """This function is used to stop the website content checking.
    """
    global is_checking_logs
    is_checking_logs = False
    logger.info("Log coroutine has been disabled.")


async def startGuildProfile(client, interaction, embed):
    """
    This function is used to check for updates on a website. It's an asyncio coroutine and should be used with await.

    Args:
        client (discord.Client): The client object that will be used to send messages
        interaction (discord.Interaction): The interaction object that will be used to send messages
        embed (str): The previous content of the website.

    Returns:
        None: This function does not return anything. It runs indefinitely.
    """
    # Updating global previous_content with the response, if provided
    global guild_previous_embed
    guild_previous_embed = embed

    global is_checking_guild_profile
    is_checking_guild_profile = True
    logger.info("Guild profile coroutine has been enabled.")
    
    # Get message from interaction for editing the message afterwards if the guild profile was updated
    message = await client.send_message(interaction, embed)
    message_id = message.id
    channel_id = message.channel.id
    
    async def check_guild_embed() -> None:
        """
        An async function that checks if the guild's rio data has changed.

        This function fetches the website content using fetch_website_content() and then checks if it has changed.
        If it has, it sends a message through the client and updates previous_content.
        """
        global guild_previous_embed

        try:
            content = await fetch_function_data(responses.prepare_rio_guild_embed)
            
            if content != guild_previous_embed:
                # Edit the message directly
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                await message.edit(embed=content)
                guild_previous_embed = content
                logger.info("Guild embed has been updated.")
            else:
                logger.info("Guild embed has not changed.")
        except Exception as e:
            logger.error(f"An error occurred in check_website: {e}")

    while is_checking_guild_profile:
        try:
            await check_guild_embed()
            await asyncio.sleep(3600)  # Wait for 1 hour
        except Exception as e:
            logger.error(f"An error occurred in check_update: {e}")
            
async def stopGuildProfile():
    """This function is used to disable the guild profile checking.
    """
    global is_checking_guild_profile
    is_checking_guild_profile = False
    logger.info("Guild profile coroutine has been disabled.")
