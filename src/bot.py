import os

import discord

from src import log, responses
from src.aclient import client

logger = log.setup_logger(__name__)

def run_discord_bot():
    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    @client.tree.command(name="logs", description="Returns the link to the latest logs")
    async def logs(interaction: discord.Interaction):
        response = await responses.response_latest(client)
        await client.send_message(interaction, response)

    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""" **BASIC COMMANDS** \n
        - `/logs` Returns the link to the latest logs.

        For complete documentation, please visit:
        https://github.com/lvlcn-t/log_tx""")

        logger.info(
            "\x1b[31mSomeone needs help!\x1b[0m")
        

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)