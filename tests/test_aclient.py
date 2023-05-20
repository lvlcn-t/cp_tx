import asyncio
import discord
from discord import app_commands
from unittest import mock
from src import aclient

import pytest

@pytest.fixture
def mock_interaction():
    interaction = mock.MagicMock(spec=discord.Interaction)
    interaction.followup.send = mock.AsyncMock()
    return interaction


@pytest.fixture
def mock_embed():
    """Create a mock embed object for testing"""
    embed = mock.MagicMock(spec=discord.Embed)
    return embed

def test_aclient_init():
    # Test if aclient is being initialized correctly
    client = aclient.aclient()

    assert isinstance(client.tree, app_commands.CommandTree)
    assert client.intents.message_content is True
    assert isinstance(client.activity, discord.Activity)

@pytest.mark.asyncio
async def test_send_message_with_embed(event_loop, mock_interaction, mock_embed):
    # Test if send_message works correctly with Embed
    client = aclient.aclient()
    mock_embed_inst = mock_embed()

    message = await client.send_message(mock_interaction, mock_embed_inst)

    assert mock_interaction.followup.send.call_args.args[0] == mock_embed_inst
    assert message == mock_interaction.followup.send.return_value

@pytest.mark.asyncio
async def test_send_message_with_str(event_loop, mock_interaction):
    # Test if send_message works correctly with string
    client = aclient.aclient()

    message = await client.send_message(mock_interaction, "Test message")

    mock_interaction.followup.send.assert_called_once_with("Test message")
    assert message == mock_interaction.followup.send.return_value

@pytest.mark.asyncio
async def test_send_message_exception_handling(event_loop, mock_interaction):
    # Test if exceptions during message sending are correctly handled
    client = aclient.aclient()
    mock_interaction.followup.send.side_effect = Exception("Test exception")

    with pytest.raises(Exception, match="Test exception"):
        await client.send_message(mock_interaction, "Test message")
