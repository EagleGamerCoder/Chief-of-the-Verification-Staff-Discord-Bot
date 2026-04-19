'''

Module: embeds.py
Author: EagleGamerCoder
Most recent update version: V 0.5.1
Description:
    Creates and returns all embeds used by the bot.

Usage:
    verify_view.py
    discord_roblox_role_sync.py

Components:
    Functions:
        create_verification_embed() -> discord.Embed
        create_server_rules_embed() -> discord.Embed
        create_role_output_embed(roles : list) -> discord.Embed

    Classes:
        _

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord

# Modules


# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Creates a Embed for verifing discord users
def create_verification_embed() -> discord.Embed:
    return discord.Embed(
        title="- Roblox Verification -",
        description="1. React with a '✅' to the message in the '📘・server-rules' channel.\n"
        "2. Click the 'Start Verification' button below. \n\n"
        "> If you are already Verified click 'Update' to update your server roles.",
        color=discord.Color(0xffd739)
    )



# Creates a Embed for the server rules
def create_server_rules_embed() -> discord.Embed:
    return discord.Embed(
        description="1. **ALL** Not-Safe-For-Work (NSFW) content or actions are prohibited.\n"
            "2. **DO NOT** Spam anything on any channels.\n"
            "3. Be kind to **EVERYONE** on this server, we don't want bullying of any sort.\n"
            "4. **NO** Abusing any power as you are privileged to have it :slight_smile: . \n"
            "5. **DO NOT** Make fake bug reports or post dumb ideas on ideas-and-suggestions.\n"
            "6. **NO** Excessive profanity.\n"
            "7. **NO** Discriminatory language or profanity.\n"
            "8. **ALL** Forms of Online dating are prohibited.\n"
            "9. **NO** Pinging Command or High ranking staff.\n"
            "10. **NO** Advertisement unless by command staff.\n"
            "11. **DO NOT** Attempt to hack or exploit any moderation or other systems.\n"
            "12. **DO NOT** Share any personal information with anyone, or ask someone for their Personal Information.\n\n"
            "> Ask someone or reach out to our development team, if you have any *important* questions about the rules.\n\n"
            "## If ANY of these rules are broken, appropriate action will be taken depending on the severity and frequency of the offense. This may include a warning, mute, kick, or ban from the server.", 
        color=discord.Color(0xffd739)
    )



# Creates a Embed for the output of sync_discord_and_roblox_roles
def create_role_output_embed(roles : list) -> discord.Embed:
    role_list = "\n".join(roles)
    
    return discord.Embed(
        description=f"You have been given the roles:\n\n{role_list}",
        color=discord.Color(0xffd739)
    )