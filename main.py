'''

Chief-Of-The-Verification-Staff

A Discord Bot that creates a built-in embed to verify, update users roles and present server rules in the Calderian Army Discord Servers

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import asyncio

# Modules
import db
import webserver
import logging

from config import discord_token
from bot.bot import Class_bot
from bot.context import BotContext
from utils.logging import log_error
from views.verify_view import VerifyView
from views.embeds import (
    create_server_rules_embed,
    create_verification_embed,
)

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

async def main():
    print("[SETUP] Setup starting...")

    # ---------- Init database ----------

    print(f"[SETUP] Initialising database...")
    db.init_database()
    print(f"[SETUP] Initialised database!")

    # ---------- Bot creation ----------
    
    print(f"[SETUP] Creating bot...")
    bot = Class_bot()

    print(f"[SETUP] Loading bot modules...")
    context = BotContext(
        db=db,
        log_error=log_error,
        create_server_rules_embed=create_server_rules_embed,
        create_verification_embed=create_verification_embed,
        VerifyView=VerifyView
    )

    await bot.load_modules(context)
    print(f"[SETUP] Loaded bot modules!")

    print(f"[SETUP] Created bot!")

    # ---------- Bot startup ----------

    print(f"[SETUP] Starting bot...")

    await asyncio.gather(
        webserver.start_webserver(),
        bot.start(discord_token)
    )
    

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    asyncio.run(main())