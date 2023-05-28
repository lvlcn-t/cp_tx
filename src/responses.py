from src import log, raiderio
import os
import discord

# Initialize logger
logger = log.setup_logger(__name__)


async def prepare_rio_guild_embed():
    raid_progression, boss_names, latest_boss_kill_links = await raiderio.guild_profile()
    
    if raid_progression != "> **ERROR: Something went wrong, please try again …":
        # Create embed message.
        embed = discord.Embed(
            title="Casual Progress",
            color=0x00FFFF,
            url="https://raider.io/guilds/eu/eredar/Casual%20Progress",
        )
        embed.set_thumbnail(
            url="https://render.worldofwarcraft.com/eu/guild/crest/114/emblem-114-b1b8b1-232323.jpg"
        )
        embed.set_author(
            name="Casual Progress Bot",
            url="https://worldofwarcraft.blizzard.com/en-gb/guild/eu/eredar/casual-progress",
            icon_url="https://render.worldofwarcraft.com/eu/guild/crest/114/emblem-114-b1b8b1-232323.jpg",
        )

        # Add raid progression to embed.
        embed.add_field(
            name=f"Current Progress: { list(raid_progression['raid_progression'].values())[0]['summary'] }", # type: ignore
            value="",
            inline=False,
        )
        for raid_index, (raid, summary) in enumerate(raid_progression["raid_progression"].items()): # type: ignore
            # Format raid progress summary with corresponding emoji.
            if "N" in summary["summary"]:
                summary["summary"] = "\U0001F7E2 " + summary["summary"]
            elif "H" in summary["summary"]:
                summary["summary"] = "\U0001F535 " + summary["summary"]
            elif "M" in summary["summary"]:
                summary["summary"] = "\U0001F7E3 " + summary["summary"]

            raid_name = raid.replace("-", " ").title()

            # Add raid progress to embed.
            embed.add_field(
                name=f"{raid_name}:", value=f"Latest Kill: [{boss_names[raid_index]}]({latest_boss_kill_links[raid_index]})", inline=True
            )

            # Add latest boss kill to embed.
            embed.add_field(
                name=f"{summary['summary']}", 
                value="", 
                inline=True
            )

            embed.add_field(name="", value="", inline=False)

        # Send embed message.
        return embed
    else:
        # Send error message.
        return raid_progression
