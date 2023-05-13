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
        await interaction.response.defer(ephemeral=False)
        response = await responses.response_latest(client)
        await client.send_message(interaction, response)

    @client.tree.command(name="bug", description="Report a bug")
    async def bug(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, "For more infos check your DMs.")

        with open("./.github/ISSUE_TEMPLATE/bug_report.md", "r") as f:
            bug_report_template = f.read()

        # Send a DM to the user asking for more information about the bug
        await interaction.user.send("Hi there! I'm sorry to hear that you're experiencing a bug. Can you please provide me with these information so I can help you?\n```" + bug_report_template + "```")

        # Get the user's response
        response = await interaction.user.wait_for("message")

        # Thank the user for their report
        await interaction.user.send("Thank you for your report! We'll look into it and get back to you as soon as possible.")

    @client.tree.command(name="request_feature", description="Request a feature")
    async def req_feature(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, "For more infos check your DMs.")

        with open("./.github/ISSUE_TEMPLATE/feature_request.md", "r") as f:
            feature_request_template = f.read()

        # Send a DM to the user asking for more information about the bug
        await interaction.user.send("Hi there! I'm looking forward to hear that your feature request. Can you please provide me with these details?\n```" + feature_request_template + "```")

        # Get the user's response
        response = await interaction.user.wait_for("message")

        # Thank the user for their report
        await interaction.user.send("Thank you for your request! We'll look into it!")

    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""" **BASIC COMMANDS** \n- `/logs` Returns the link to the latest logs.\nFor complete documentation, please visit:\nhttps://github.com/lvlcn-t/cp_tx""")

        logger.info(
            "\x1b[31mSomeone needs help!\x1b[0m")
        

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)