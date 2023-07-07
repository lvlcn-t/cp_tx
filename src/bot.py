import os
import discord
import asyncio
from discord import app_commands
from asyncio import TimeoutError
from datetime import datetime
from dateutil.parser import parse, ParserError
from polylog import setup_logger, trace_id_var

from src import responses, gh, bot_coroutines, warcraftlogs
from src.aclient import client

# Setting up the logger for the discord bot
logger = setup_logger(__name__)


# Function to run the discord bot
def run_discord_bot():
    # Event triggered when the bot is ready
    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f"{client.user} is now running!")
        
        if os.getenv("DISCORD_CHANNEL_ID_LOGS") is not None:
            if not client.is_task_running("logs_routine"):
                trace_id_var.set(0) # type: ignore
                client.running_tasks["logs_routine"] = asyncio.create_task(bot_coroutines.startLogs(client, None))
        
        if os.getenv("DISCORD_CHANNEL_ID_PROFILE") is not None and os.getenv("DISCORD_MESSAGE_ID_PROFILE") is not None:
            if not client.is_task_running("rio_routine"):
                trace_id_var.set(0) # type: ignore
                client.running_tasks["rio_routine"] = asyncio.create_task(bot_coroutines.startGuildProfile(client, None, None))

    # * Command to get the latest logs
    @client.tree.command(name="logs", description="Returns the link to the latest logs")
    @app_commands.choices(choices=
        [
            app_commands.Choice(name="Start log coroutine", value="start"),
            app_commands.Choice(name="Stop log coroutine", value="stop")
        ]
    )
    async def logs(interaction: discord.Interaction, choices: app_commands.Choice[str]):
        if interaction.user.guild_permissions.administrator: # type: ignore
            await interaction.response.defer(ephemeral=True)
            # Start or stop the logs coroutine loop based on the action parameter
            if choices.value == "start":
                trace_id_var.set(interaction.user.id) # type: ignore
                if not client.is_task_running("logs_routine"):
                    await client.send_message(interaction, "Logs started.")
                    await bot_coroutines.startLogs(client, interaction)
                else:
                    await client.send_message(interaction, "Routine is already running")
                    logger.info(f"{interaction.user.name} tried to create another instance of the log coroutine")
                    
            elif choices.value == "stop":
                # Stop the coroutine
                await bot_coroutines.stopLogs()
                await client.send_message(interaction, "Logs stopped.")
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    # * Command to get the logs from a specific date
    @client.tree.command(name="logs-from", description="Returns the link to the logs from a specific date")
    async def logs_date(interaction: discord.Interaction, date: str):
        try:
            parsed_date = parse(date).date()
        except ParserError:
            await interaction.response.defer(ephemeral=True)
            await client.send_message(interaction, "Invalid date format. Please enter a real date.")
            logger.info(f"{interaction.user.display_name} entered a false date.")
            return
        # Ensure the user has the 'Raidmember' role or a higher role
        user_roles = [role.name for role in interaction.user.roles]   # type: ignore
        authorized_roles: list[str] = ["Raidmember", "Ehemalige Raider", "Raidbewerber", "Offis", "Leitung"]
        
        if any(role in user_roles for role in authorized_roles): # type: ignore
            await interaction.response.defer(ephemeral=True)
            await client.send_message(interaction, f"Logs from {date}:\n{await warcraftlogs.logs_from(parsed_date)}")
            logger.info(f"Found logs from {date} for {interaction.user.display_name}.")
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    # * Command to get the guild raider.io profile
    @client.tree.command(name="guild-profile", description="Returns the link to the guilds raider.io profile")
    @app_commands.choices(choices=
        [
            app_commands.Choice(name="Show once", value="once"),
            app_commands.Choice(name="Start coroutine", value="start"),
            app_commands.Choice(name="Stop coroutine", value="stop")
        ]
    )
    async def rio_guild_profile(interaction: discord.Interaction, choices: app_commands.Choice[str]):
        """
        Asynchronously handles the "rio-guild" command. Sends a message containing the guild's raider.io profile.
        
        Args:
            interaction (discord.Interaction): The interaction object containing the command data.
            coroutine (bool, optional): If True, start the coroutine loop to periodically check for updates. Defaults to False.
        """
        if choices.value == "once":
            await interaction.response.defer(ephemeral=False)
            response = await responses.prepare_rio_guild_embed()
            # Send the embed message
            await client.send_message(interaction, response)

        elif choices.value == "start":
            if interaction.user.guild_permissions.administrator: # type: ignore
                # Start the coroutine
                await interaction.response.defer(ephemeral=True)
                if not client.is_task_running("rio_routine"):
                    response = await responses.prepare_rio_guild_embed()
                    await client.send_message(interaction, "Started guild profile coroutine.")
                    await bot_coroutines.startGuildProfile(client, interaction, response)
                else:
                    await client.send_message(interaction, "Routine is already running")
                    logger.info(f"{interaction.user.name} tried to create another instance of the rio guild coroutine")
            else:
                await interaction.response.send_message(
                    "You do not have permission to use this command.", ephemeral=True
                )

        elif choices.value == "stop":
            if interaction.user.guild_permissions.administrator: # type: ignore
                # Stop the coroutine
                await interaction.response.defer(ephemeral=True)
                await bot_coroutines.stopGuildProfile()
                await client.send_message(interaction, "Stopped guild profile coroutine.")
            else:
                await interaction.response.send_message(
                    "You do not have permission to use this command.", ephemeral=True
                )

        else:
            await interaction.response.defer(ephemeral=True)
            await client.send_message(interaction, "Invalid action.")
            logger.warning(f"Invalid action: {choices.value}")

    # * Command to get the guild's raidbots account credentials
    @client.tree.command(name="raidbots", description="Display the Login credentials of our guild's raidbots account")
    async def raidbots(interaction: discord.Interaction):
        # Ensure the user has the 'Raidmember' role or a higher role
        user_roles = [role.name for role in interaction.user.roles]   # type: ignore
        authorized_roles = ["Raidmember", "Offis", "Leitung"]
        
        raidbots_username = os.getenv("RAIDBOTS_USERNAME")
        raidbots_password = os.getenv("RAIDBOTS_PASSWORD")
        
        if any(role in user_roles for role in authorized_roles) or interaction.user.guild_permissions.administrator: # type: ignore
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(
                f"The Login credentials for our [Raidbots](https://www.raidbots.com) account are:\n{raidbots_username}\n{raidbots_password}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    # * Command to move all users from one voice channel to another
    @client.tree.command(name="move", description="Move all users from one voice channel to another")
    async def move(interaction: discord.Interaction, source: discord.VoiceChannel, destination: discord.VoiceChannel):
        # Only allow administrators to use this command
        if interaction.user.guild_permissions.administrator: # type: ignore
            await interaction.response.defer(ephemeral=True)
            
            if source is None or destination is None or source == destination:
                await interaction.followup.send("You didn't give the necessary channels.", ephemeral=True)
                return
            
            # Move all members in the from_channel to the to_channel
            try:
                for member in source.members:
                    await member.move_to(channel=destination)
            except Exception as e:
                logger.error(f"Failed to move all members from {source} to {destination}. Reason: { e }")
            
            await interaction.followup.send(
                f"Moved all members from {source} to {destination}.", ephemeral=True
            )
            logger.info(f"Moved all members from {source} to {destination}.")

        else:
            await interaction.followup.send(
                "You do not have permission to use this command.", ephemeral=True
            )
            logger.warning(f"Invalid action: {interaction.user.guild_permissions.administrator}") # type: ignore

    # * Command to report a bug
    @client.tree.command(name="bug", description="Report a bug")
    async def bug(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(
            interaction,
            """
**For more infos check your DMs.**\n\n \
If you don't have a DM from me, you need to activate this **Allow direct messages from server members** in your settings: \n \
User Settings -> Privacy & Safety -> Server Privacy Defaults""",
        )

        # Opens the bug_report.md file
        with open("./.github/ISSUE_TEMPLATE/bug_report.md", "r") as f:
            bug_report_template = f.read()

        # Lines to be removed from the bug report template
        lines_to_remove = [
            "name: Bug report\n",
            "about: Create a report to help us improve\n",
            "labels: ''\n",
            "assignees: ''\n",
            "**Screenshots**\nIf applicable, add screenshots to help explain your problem.\n",
        ]

        user_friendly_template = gh.clean_template(bug_report_template, lines_to_remove)
        # Sends a DM to the user asking for more information about the bug
        await interaction.user.send(
            "Hi there! I'm sorry to hear that you're experiencing a bug.\nCan you please provide me with **this information** so I can help you?\n```markdown\n"
            + user_friendly_template
            + "```"
        )

        response = None
        correct_response = False
        try:
            # Waits for the user's response
            while correct_response is False:
                response = await client.wait_for(
                    "message", check=check_author(interaction.user)
                )
                if not gh.validate_response(response.content):
                    await interaction.user.send(
                        "Your response does not follow the specified template. Please try again using the correct format."
                    )
                else:
                    correct_response = True
        except TimeoutError:
            await interaction.user.send("You did not reply in time, please try again.")
            logger.info(
                f"\x1b[31m{interaction.user.name} took to long to respond with its bug report!\x1b[0m"
            )
            return

        # Extract author information
        try:
            author = {
                "name": interaction.user.name,
                # ! Discriminators will be deprecated after the roll out of the new username feature
                "discriminator": interaction.user.discriminator,
            }
            title, body = gh.get_response_info(
                response, author["name"], author["discriminator"]
            )

        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = gh.get_response_info(response, author)

        labels = ["bug"]

        await gh.create_github_issue(str(title), body, labels)

        # Thanks the user for their report
        await interaction.user.send(
            "Thank you for your report! We'll look into it and get back to you as soon as possible."
        )
        logger.info(f"\x1b[31m{interaction.user.name} reportet a bug!\x1b[0m")

    # * Command to request a feature
    @client.tree.command(name="request-feature", description="Request a feature")
    async def req_feature(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await client.send_message(
            interaction,
            """
**For more infos check your DMs.**\n\n \
If you don't have a DM from me, you need to activate this **Allow direct messages from server members** in your settings: \n \
User Settings -> Privacy & Safety -> Server Privacy Defaults""",
        )

        # Opens the feature_request.md file
        with open("./.github/ISSUE_TEMPLATE/feature_request.md", "r") as f:
            feature_request_template = f.read()

        # Lines to be removed from the feature request template
        lines_to_remove = [
            "name: Feature request\n",
            "about: Suggest an idea for this project\n",
            "labels: ''\n",
            "assignees: ''\n",
        ]

        user_friendly_template = gh.clean_template(
            feature_request_template, lines_to_remove
        )
        # Sends a DM to the user asking for more information about the feature request
        await interaction.user.send(
            "Hi there! I'm looking forward to hear that your feature request.\nCan you please provide me with **these details**?\n```markdown\n"
            + user_friendly_template
            + "```"
        )

        response = None
        correct_response = False
        try:
            # Waits for the user's response
            while correct_response is False:
                response = await client.wait_for(
                    "message", check=check_author(interaction.user)
                )
                if not gh.validate_response(response.content):
                    await interaction.user.send(
                        "Your response does not follow the specified template. Please try again using the correct format."
                    )
                else:
                    correct_response = True
        except TimeoutError:
            await interaction.user.send("You did not reply in time, please try again.")
            logger.info(
                f"\x1b[31m{interaction.user.name} took to long to respond with its feature request!\x1b[0m"
            )
            return

        # Extract author information
        try:
            author = {
                "name": interaction.user.name,
                # ! Discriminators will be deprecated after the roll out of the new username feature
                "discriminator": interaction.user.discriminator,
            }
            title, body = gh.get_response_info(
                response, author["name"], author["discriminator"]
            )

        except Exception as e:
            logger.warning(f"Failed to extract author details: {e}")
            author = interaction.user.name
            title, body = gh.get_response_info(response, author)

        labels = ["feature"]

        await gh.create_github_issue(str(title), body, labels)

        # Thanks the user for their feature request
        await interaction.user.send("Thank you for your request! We'll look into it!")
        logger.info(f"\x1b[31m{interaction.user.name} requested a feature!\x1b[0m")

    # * Command to get help for the bot
    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("""
### **BASIC COMMANDS**

- `/logs [start|stop]`: Starts or stops the logging coroutine. Only for users with administrator permissions.
  - **start**: Begins the logging coroutine.
  - **stop**: Stops the logging coroutine.
  
- `/logs-from [date]`: Returns the logs from a given date. Only for users with the role "Raidbewerber" or higher.

- `/guild-profile [once|start|stop]`: Shows the guild's raider.io profile.
  - **once**: Sends the guild's raider.io profile as a message. Only for users with the role "Raidbewerber" or higher.
  - **start**: Begins a coroutine to periodically update the guild's embed with the new raider.io profile information. Only for users with administrator permissions.
  - **stop**: Stops the raider.io profile update coroutine. Only for users with administrator permissions.

- `/move [source] [destination]`: Moves all users from one channel to another. Only for users with administrator permissions.

- `/raidbots`: Shows the login credentials of the raidbots account. Only for users with the role "Raidmember" or higher.

- `/bug`: Report a bug.
    - After sending this command, the bot will direct message you asking for details about the bug.

- `/request-feature`: Request a feature.
    - After sending this command, the bot will direct message you asking for details about the feature request.

For complete documentation, please visit:\nhttps://github.com/lvlcn-t/cp_tx
        """)
        logger.info("\x1b[31mSomeone needs help!\x1b[0m")

    # Get the bot token from environment variables
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    # Run the bot
    client.run(str(TOKEN))


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
        return message.author == author and isinstance(
            message.channel, discord.DMChannel
        )

    return inner_check
