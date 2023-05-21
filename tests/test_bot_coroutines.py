# import pytest
# from src import bot_coroutines, warcraftlogs, responses
# from unittest.mock import patch, MagicMock
# import discord

# @pytest.fixture
# def mock_client():
#     client = MagicMock(spec=discord.Client)
#     return client

# @pytest.fixture
# def mock_interaction():
#     interaction = MagicMock(spec=discord.Interaction)
#     return interaction

# @patch("src.bot_coroutines.fetch_function_data")
# @patch("src.bot_coroutines.logger")
# @pytest.mark.asyncio
# async def test_startLogs(mock_logger, mock_fetch_function_data, mock_client, mock_interaction):
#     # Arrange
#     mock_fetch_function_data.return_value = "latest logs"
#     expected_logs = "latest logs"
    
#     # Act
#     await bot_coroutines.startLogs(mock_client, mock_interaction, expected_logs)

#     # Assert
#     mock_client.get_channel.assert_called_once_with(mock_interaction.channel_id)
#     mock_client.send_message.assert_called_once_with(mock_interaction, expected_logs)
#     mock_logger.info.assert_called_with("Log coroutine has been enabled.")
#     assert bot_coroutines.is_checking_logs

# @patch("src.bot_coroutines.logger")
# @pytest.mark.asyncio
# async def test_stopLogs(mock_logger):
#     # Act
#     await bot_coroutines.stopLogs()

#     # Assert
#     mock_logger.info.assert_called_once_with("Log coroutine has been disabled.")
#     assert not bot_coroutines.is_checking_logs

# @patch("src.bot_coroutines.fetch_function_data")
# @patch("src.bot_coroutines.logger")
# @pytest.mark.asyncio
# async def test_startGuildProfile(mock_logger, mock_fetch_function_data, mock_client, mock_interaction):
#     # Arrange
#     mock_fetch_function_data.return_value = "latest guild profile"
#     expected_guild_profile = "latest guild profile"
    
#     # Act
#     await bot_coroutines.startGuildProfile(mock_client, mock_interaction, expected_guild_profile)

#     # Assert
#     mock_client.send_message.assert_called_once_with(mock_interaction, expected_guild_profile)
#     mock_logger.info.assert_called_once_with("Guild profile coroutine has been enabled.")
#     assert bot_coroutines.is_checking_guild_profile

# @patch("src.bot_coroutines.logger")
# @pytest.mark.asyncio
# async def test_stopGuildProfile(mock_logger):
#     # Act
#     await bot_coroutines.stopGuildProfile()

#     # Assert
#     mock_logger.info.assert_called_once_with("Guild profile coroutine has been disabled.")
#     assert not bot_coroutines.is_checking_guild_profile
