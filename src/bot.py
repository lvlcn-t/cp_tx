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
        response = await responses.latest_wc_logs(client)
        await client.send_message(interaction, response)

    @client.tree.command(name="bug", description="Report a bug")
    async def bug(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, "For more info, check your DMs.")

        with open("./.github/ISSUE_TEMPLATE/bug_report.md", "r") as f:
            bug_report_template = f.read()

        # Remove specific lines from the template
        lines_to_remove = [
            "name: Bug report\n",
            "about: Create a report to help us improve\n",
            "labels: ''\n",
            "assignees: ''\n",
            "**Screenshots**\nIf applicable, add screenshots to help explain your problem.\n"
        ]

        user_friendly_template = clean_template(bug_report_template, lines_to_remove)
        # Send a DM to the user asking for more information about the bug
        await interaction.user.send("Hi there! I'm sorry to hear that you're experiencing a bug.\nCan you please provide me with **this information** so I can help you?\n```markdown\n" + user_friendly_template + "```")

        # Get the user's response
        response = await client.wait_for("message")

        title, body = get_respose_info(response, interaction.user.name)

        # ! user.discriminator will be deprecated after the roll out of the new username feature
        try:
            author = {
                'name': interaction.user.name,
                'discriminator': interaction.user.discriminator
            }
            title, body = get_respose_info(response, author['name'], author['discriminator'])
        
        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = get_respose_info(response, author)
        
        labels = ["bug"]

        await responses.create_github_issue(str(title), body, labels)

        # Thank the user for their report
        await interaction.user.send("Thank you for your report! We'll look into it and get back to you as soon as possible.")


    @client.tree.command(name="request-feature", description="Request a feature")
    async def req_feature(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, "For more infos check your DMs.")

        with open("./.github/ISSUE_TEMPLATE/feature_request.md", "r") as f:
            feature_request_template = f.read()

        # Remove specific lines from the template
        lines_to_remove = [
        "name: Feature request\n",
        "about: Suggest an idea for this project\n",
        "labels: ''\n",
        "assignees: ''\n"
        ]

        user_friendly_template = clean_template(feature_request_template, lines_to_remove)
        # Send a DM to the user asking for more information about the bug
        await interaction.user.send("Hi there! I'm looking forward to hear that your feature request.\nCan you please provide me with **these details**?\n```" + user_friendly_template + "```")

        # Get the user's response
        response = await client.wait_for("message")
        
        # ! user.discriminator will be deprecated after the roll out of the new username feature
        try:
            author = {
                'name': interaction.user.name,
                'discriminator': interaction.user.discriminator
            }
            title, body = get_respose_info(response, author['name'], author['discriminator'])
        
        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = get_respose_info(response, author)

        labels = ["feature"]

        await responses.create_github_issue(str(title), body, labels)

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


def clean_template(template:str, lines_to_remove:list):
    """_summary_

    Args:
        template (str): _description_
        lines_to_remove (list): The lines that need to be removed out of the template

    Returns:
        str: The template with the provided lines removed
    """

    for line in lines_to_remove:
        template = template.replace(line, "")

    return template

def get_respose_info(response, author_name, author_discriminator=None):
    """_summary_

    Args:
        response (_type_): _description_
        author_name (_type_): _description_
        author_discriminator (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    # Extract information from the user's response
    lines = response.content.split("\n")
    title = None
    body = ""
    is_body = False
    for line in lines:
        if line.startswith("title:"):
            title = line.replace("title:", "").strip()
            title = title.replace("'", "")
        elif line.strip() == "---" and not is_body:
            is_body = True
        elif is_body and not line.strip() == "---":
            body += line + "\n"
    
    if author_discriminator is not None:
        body += f"\n\n**From: {author_name}#{author_discriminator}**"
    else:
        body += f"\n\n**From: @{author_name}**"

    return title, body