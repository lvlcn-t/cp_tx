import os
import discord
from src import log
from dotenv import load_dotenv
from discord import app_commands

logger = log.setup_logger(__name__)
load_dotenv()

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.listening, name="/logs | /help")


    async def send_message(self, interaction, response):
        try:
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(response)
        except Exception as e:
            await interaction.followup.send(f"> **ERROR: Something went wrong, please try again later!** \n ```ERROR MESSAGE: {e}```")
            logger.exception(f"Error while sending message: {e}")


client = aclient()
