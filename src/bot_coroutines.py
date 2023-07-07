from src import warcraftlogs, responses
import asyncio
from datetime import datetime
import os
from polylog import setup_logger, span_id_var
from typing import Union, Callable, Optional
import discord

# Initialize logger
logger = setup_logger(__name__)

guild_previous_embed: Union[None, discord.Embed] = None
logs_previous_content: Union[None, str] = None
is_checking_logs: Union[None, bool] = None
is_checking_guild_profile: Union[None, bool] = None

async def fetch_function_data(callback_function: Callable) -> Union[None, discord.Embed, str]:
        """
        An async function to fetch a functions response.

        Args:
            callback_function (Callable): The function to call to get the data.

        Returns:
            data: The data returned by the callback_function.
        """
        data = await callback_function()
        return data

async def startLogs(client: discord.Client, interaction: discord.Interaction, response=None) -> None:
    """
    This function is used to check for updates on a website. It's an asyncio coroutine and should be used with await.

    Args:
        client (discord.Client): The client object that will be used to send messages
        interaction (discord.Interaction, None): The interaction object that will be used to send messages
        response (str, optional): The previous content of the website. Defaults to None.

    Returns:
        None: This function does not return anything. It runs indefinitely.
    """
    # Updating global previous_content with the response, if provided
    global logs_previous_content
    logs_previous_content = response
    
    global is_checking_logs
    is_checking_logs = True
    if interaction is not None:
        span_id_var.set(interaction.channel_id) # type: ignore
    else:
        span_id_var.set(int(os.getenv("DISCORD_CHANNEL_ID_LOGS"))) # type: ignore
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
                content: Union[None, str, discord.Embed] = await fetch_function_data(warcraftlogs.latest_logs)

                if content != logs_previous_content:
                    # Website content has changed
                    # Get the channel from the interaction's channel_id and send the message to the channel directly
                    if interaction is not None:
                        channel: Optional[Union[discord.abc.GuildChannel, discord.Thread, discord.abc.PrivateChannel]] = client.get_channel(interaction.channel_id) # type: ignore
                    else:
                        try:
                            channel_id = int(os.getenv("DISCORD_CHANNEL_ID_LOGS")) # type: ignore
                            channel = client.get_channel(channel_id)
                        except Exception as e:
                            logger.exception(f"DISCORD_CHANNEL_ID_LOGS is not an integer: {e}")
                            raise TypeError("DISCORD_CHANNEL_ID_LOGS is not an integer.")
                    
                    await channel.send(content) # type: ignore
                    logs_previous_content = str(content)
                    logger.info("Website content has been updated.")
                else:
                    logs_previous_content = str(content)
                    logger.info("Website content has not changed.")
            except Exception as e:
                logger.error(f"An error occurred in check_website: {e}")
        else:
            logger.debug("Not the right time for checking the website content.")

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
    is_checking_logs = bool(False)
    logger.info("Log coroutine has been disabled.")


async def startGuildProfile(client: discord.Client, interaction: discord.Interaction, embed: Union[None, discord.Embed]) -> None:
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
    guild_previous_embed: Union[None, discord.Embed] = embed

    global is_checking_guild_profile
    is_checking_guild_profile = True
    
    if interaction is not None:
        span_id_var.set(interaction.channel_id) # type: ignore
    else:
        span_id_var.set(int(os.getenv("DISCORD_CHANNEL_ID_PROFILE"))) # type: ignore
    logger.info("Guild profile coroutine has been enabled.")
    
    # Get message from interaction for editing the message afterwards if the guild profile was updated
    if interaction is not None and embed is not None:
        message: Union[None, Optional[discord.WebhookMessage]] = await client.send_message(interaction, embed) # type: ignore because it's function of custom discord aclient class
        message_id = message.id                         # type: ignore
        channel_id = message.channel.id                 # type: ignore
    else:
        try:
            message_id: int = int(str(os.getenv("DISCORD_MESSAGE_ID_PROFILE")))
            channel_id: int = int(str(os.getenv("DISCORD_CHANNEL_ID_PROFILE")))
        except Exception as e:
            logger.exception(f"DISCORD_MESSAGE_ID_PROFILE or DISCORD_CHANNEL_ID_PROFILE are not an integer: {e}")
            raise TypeError("DISCORD_MESSAGE_ID_PROFILE or DISCORD_CHANNEL_ID_PROFILE not an integer")
            
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
                message = await channel.fetch_message(message_id) # type: ignore
                await message.edit(embed=content) # type: ignore
                guild_previous_embed = content # type: ignore
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
    is_checking_guild_profile = bool(False)
    logger.info("Guild profile coroutine has been disabled.")
