import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from polylog import setup_logger

# Initialize logger
logger = setup_logger(__name__)
# Load environment variables from a .env file
load_dotenv()


class aclient(discord.Client):
    """Custom discord client class for handling specific bot functionalities.

    This class is a subclass of discord.Client and includes methods for sending messages,
    and handling the bot's status/activity.
    """

    def __init__(self) -> None:
        """Initializes the aclient class.

        This involves setting up the intents (events the bot should listen to),
        the command tree (for handling commands), and the bot's activity (visible to users in Discord).
        """
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True

        # Initialize the superclass with the created intents
        super().__init__(intents=intents)

        # Create a CommandTree instance for handling commands
        self.tree = app_commands.CommandTree(self)

        # Set the bot's activity
        self.activity = discord.Activity(
            type=discord.ActivityType.listening, name="/help"
        )

    async def send_message(self, interaction, response):
        """Sends a follow-up message in response to an interaction.

        Args:
            interaction: The interaction to which the bot should respond.
            response: The response message or embed to send.
            
        Returns:
            message: The Message object that was sent.
        """
        try:
            # Try to send the response
            if isinstance(response, discord.Embed):
                message = await interaction.followup.send(embed=response)
            else:
                message = await interaction.followup.send(response)

            return message  # Return the Message object

        except Exception as e:
            # If an error occurs, send an error message and log the exception
            await interaction.followup.send(
                f"> **ERROR: Something went wrong, please try again later!**"
            )
            logger.exception(f"Error while sending message: {e}")


# Create an instance of the custom client class
client = aclient()
