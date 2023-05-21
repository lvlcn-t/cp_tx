import pytest
import discord
from discord import app_commands
from src.aclient import client
from src import bot
from unittest.mock import MagicMock

# @pytest.fixture
# def mock_interaction():
#     interaction = MagicMock(spec=discord.Interaction)
#     interaction.user.guild_permissions.administrator = True
#     return interaction

# @pytest.fixture
# def mock_choice_start():
#     choice = MagicMock(spec=app_commands.Choice)
#     choice.value = "start"
#     return choice

# @pytest.fixture
# def mock_choice_stop():
#     choice = MagicMock(spec=app_commands.Choice)
#     choice.value = "stop"
#     return choice

# @pytest.mark.asyncio
# async def test_logs_start(mock_interaction, mock_choice_start):
#     await logs(mock_interaction, mock_choice_start)
#     mock_interaction.response.defer.assert_called_once_with(ephemeral=True)
#     client.send_message.assert_called_once_with(mock_interaction, "Logs started.")
#     # Add an assertion for bot_coroutines.startLogs if desired

# @pytest.mark.asyncio
# async def test_logs_stop(mock_interaction, mock_choice_stop):
#     await logs(mock_interaction, mock_choice_stop)
#     mock_interaction.response.defer.assert_called_once_with(ephemeral=True)
#     client.send_message.assert_called_once_with(mock_interaction, "Logs stopped.")
#     # Add an assertion for bot_coroutines.stopLogs if desired

# @pytest.mark.asyncio
# async def test_rio_guild_profile_once(mock_interaction, mock_choice_once):
#     await rio_guild_profile(mock_interaction, mock_choice_once)
#     mock_interaction.response.defer.assert_called_once_with(ephemeral=False)
#     # Add assertions for responses.prepare_rio_guild_embed and client.send_message

# @pytest.mark.asyncio
# async def test_rio_guild_profile_start(mock_interaction, mock_choice_start):
#     await rio_guild_profile(mock_interaction, mock_choice_start)
#     mock_interaction.response.defer.assert_called_once_with(ephemeral=True)
#     # Add assertions for responses.prepare_rio_guild_embed, client.send_message, and bot_coroutines.startGuildProfile

# @pytest.mark.asyncio
# async def test_rio_guild_profile_stop(mock_interaction, mock_choice_stop):
#     await rio_guild_profile(mock_interaction, mock_choice_stop)
#     mock_interaction.response.defer.assert_called_once_with(ephemeral=True)
#     client.send_message.assert_called_once_with(mock_interaction, "Stopped guild profile coroutine.")
#     # Add an assertion for bot_coroutines.stopGuildProfile if desired
