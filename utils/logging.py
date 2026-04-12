'''

Info about module

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import logging
import discord

# Modules


# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

async def log_error(interaction: discord.Interaction | None, func: str, code: int, e: Exception | str):
    msg = f"[ERROR] func={func} ({code}) | {e}"

    print(msg)
    logging.error(msg)

    if interaction:
        try:
            if interaction.response.is_done():
                await interaction.followup.send(
                    "❌ An error occurred. Please contact a developer.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ An error occurred. Please contact a developer.",
                    ephemeral=True
                )
        except Exception:
            pass

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

# File logger
file_handler = logging.FileHandler(
    filename="discord_bot.log",
    encoding="utf-8",
    mode="w"
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler]
)