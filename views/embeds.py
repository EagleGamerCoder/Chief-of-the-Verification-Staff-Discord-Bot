'''

Info about module

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord

# Modules


# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def create_verification_embed():
    return discord.Embed(
        title="- Roblox Verification -",
        description="1. React with a '✅' to the message in the '📘・server-rules' channel.\n"
        "2. Click the 'Start Verification' button below. \n\n"
        "> If you are already Verified click 'Update' to update your server roles.",
        color=discord.Color(0xffd739)
    )

def create_server_rules_embed():
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