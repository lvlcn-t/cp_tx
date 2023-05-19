import os
import discord
from asyncio import TimeoutError

from src import log, responses, check_updates
from src.aclient import client

# Setting up the logger for the discord bot
logger = log.setup_logger(__name__)

# Function to run the discord bot
def run_discord_bot():

    # Event triggered when the bot is ready
    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    # Command to get the latest logs
    @client.tree.command(name="logs", description="Returns the link to the latest logs")
    async def logs(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.defer(ephemeral=False)
            response = await responses.latest_wc_logs()
            await client.send_message(interaction, response)
            
            # Start the check_update loop
            await check_updates.check_update(client, interaction, response)
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

    # Command to report a bug
    @client.tree.command(name="bug", description="Report a bug")
    async def bug(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, """
**For more infos check your DMs.**\n\n \
If you don't have a DM from me, you need to activate this **Allow direct messages from server members** in your settings: \n \
User Settings -> Privacy & Safety -> Server Privacy Defaults""")

        # Opens the bug_report.md file
        with open("./.github/ISSUE_TEMPLATE/bug_report.md", "r") as f:
            bug_report_template = f.read()

        # Lines to be removed from the bug report template
        lines_to_remove = [
            "name: Bug report\n",
            "about: Create a report to help us improve\n",
            "labels: ''\n",
            "assignees: ''\n",
            "**Screenshots**\nIf applicable, add screenshots to help explain your problem.\n"
        ]

        user_friendly_template = clean_template(bug_report_template, lines_to_remove)
        # Sends a DM to the user asking for more information about the bug
        await interaction.user.send("Hi there! I'm sorry to hear that you're experiencing a bug.\nCan you please provide me with **this information** so I can help you?\n```markdown\n" + user_friendly_template + "```")
        
        response = None
        correct_response = False
        try:
            # Waits for the user's response
            while correct_response is False:
                response = await client.wait_for("message", check=check_author(interaction.user))
                if not validate_response(response.content):
                    await interaction.user.send("Your response does not follow the specified template. Please try again using the correct format.")
                else:
                    correct_response = True
        except TimeoutError:
            await interaction.user.send("You did not reply in time, please try again.")
            logger.info(f"\x1b[31m{interaction.user.name} took to long to respond with its bug report!\x1b[0m")
            return

        # Extract author information
        try:
            author = {
                'name': interaction.user.name,
                # ! Discriminators will be deprecated after the roll out of the new username feature
                'discriminator': interaction.user.discriminator
            }
            title, body = get_response_info(response, author['name'], author['discriminator'])
        
        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = get_response_info(response, author)
        
        labels = ["bug"]

        await responses.create_github_issue(str(title), body, labels)

        # Thanks the user for their report
        await interaction.user.send("Thank you for your report! We'll look into it and get back to you as soon as possible.")
        logger.info(f"\x1b[31m{interaction.user.name} reportet a bug!\x1b[0m")


    # Command to request a feature
    @client.tree.command(name="request-feature", description="Request a feature")
    async def req_feature(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(interaction, """
**For more infos check your DMs.**\n\n \
If you don't have a DM from me, you need to activate this **Allow direct messages from server members** in your settings: \n \
User Settings -> Privacy & Safety -> Server Privacy Defaults""")

        # Opens the feature_request.md file
        with open("./.github/ISSUE_TEMPLATE/feature_request.md", "r") as f:
            feature_request_template = f.read()

        # Lines to be removed from the feature request template
        lines_to_remove = [
        "name: Feature request\n",
        "about: Suggest an idea for this project\n",
        "labels: ''\n",
        "assignees: ''\n"
        ]

        user_friendly_template = clean_template(feature_request_template, lines_to_remove)
        # Sends a DM to the user asking for more information about the feature request
        await interaction.user.send("Hi there! I'm looking forward to hear that your feature request.\nCan you please provide me with **these details**?\n```markdown\n" + user_friendly_template + "```")

        response = None
        correct_response = False
        try:
            # Waits for the user's response
            while correct_response is False:
                response = await client.wait_for("message", check=check_author(interaction.user))
                if not validate_response(response.content):
                    await interaction.user.send("Your response does not follow the specified template. Please try again using the correct format.")
                else:
                    correct_response = True
        except TimeoutError:
            await interaction.user.send("You did not reply in time, please try again.")
            logger.info(f"\x1b[31m{interaction.user.name} took to long to respond with its feature request!\x1b[0m")
            return

        # Extract author information
        try:
            author = {
                'name': interaction.user.name,
                # ! Discriminators will be deprecated after the roll out of the new username feature
                'discriminator': interaction.user.discriminator
            }
            title, body = get_response_info(response, author['name'], author['discriminator'])
        
        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = get_response_info(response, author)

        labels = ["feature"]

        await responses.create_github_issue(str(title), body, labels)

        # Thanks the user for their feature request
        await interaction.user.send("Thank you for your request! We'll look into it!")
        logger.info(f"\x1b[31m{interaction.user.name} requested a feature!\x1b[0m")

    # Command to get help for the bot
    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("""\
**BASIC COMMANDS** \n \
- `/logs` Returns the link to the latest logs.\n \
- `/bug` Report a bug\n \
- `/request-feature` Request a feature\n \
For complete documentation, please visit:\nhttps://github.com/lvlcn-t/cp_tx""")

        logger.info("\x1b[31mSomeone needs help!\x1b[0m")
        

    # Get the bot token from environment variables
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    # Run the bot
    client.run(TOKEN)


def check_author(author):
    """Checks if a message is from the given author and if it is a direct message.

    This function returns another function that performs the checks.
    This is known as a closure.

    Args:
        author (discord.User): The author to check messages against.

    Returns:
        function: A function that takes a message, checks if it is from the specified author and if it is a direct message, and returns True or False accordingly.
    """
    def inner_check(message):
        return message.author == author and isinstance(message.channel, discord.DMChannel)
    return inner_check

def validate_response(response):
    """Validates a response to ensure it follows a specific format.

    This function checks that a response has a title line that isn't empty, and a second line consisting of '---'.

    Args:
        response (str): The response to validate.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    lines = response.split("\n")
    
    # Check if the 'title' line exists and is not empty
    title_exists = any(line.strip().lower().startswith('title:') and line.strip().lower() != 'title:' for line in lines)
    
    # Check if the second '---' line exists
    second_dash_line_exists = '---' in lines[1:]

    return title_exists and second_dash_line_exists

# Function to clean the template by removing specific lines
def clean_template(template:str, lines_to_remove:list):
    """Removes specified lines from a given template.

    Args:
        template (str): The original template.
        lines_to_remove (list): The lines that need to be removed out of the template.

    Returns:
        str: The template with the provided lines removed.
    """

    for line in lines_to_remove:
        template = template.replace(line, "")

    return template

# Function to extract relevant information from a user's response
def get_response_info(response, author_name, author_discriminator=None):
    """Extracts the title and body from a user's response.

    Args:
        response (discord.Message): User's response to the bot's request.
        author_name (str): The username of the author.
        author_discriminator (str, optional): The discriminator of the author. Defaults to None.

    Returns:
        tuple: Contains the title (str) and body (str) of the user's response.
    """

    # Extract information from the user's response
    lines = response.content.split("\n")
    title = None
    body = ""
    is_body = False
    for line in lines:
        # Use lower() to make the check case-insensitive
        if line.lower().startswith("title:"):
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
