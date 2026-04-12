'''

Chief-Of-The-Verification-Staff

V 0.2

A Discord Bot that creates a built-in embed to verify, update users roles and present server rules in the Calderian Army Discord Servers

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import asyncio

# Modules
import db
import webserver

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

    # ---------- Webserver handling ----------
    
    print(f"[SETUP] Starting webserver...")
    web_task = asyncio.create_task(webserver.start_webserver())

    web_task.add_done_callback(webserver.handle_web_result)
    print(f"[SETUP] Started webserver!")

    # ---------- Bot startup ----------

    print(f"[SETUP] Starting bot...")
    try:
        await bot.start(discord_token)
    finally:
        await bot.close()

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

if __name__ == '__main__':
    asyncio.run(main())