'''

info

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord
import importlib
import os

from discord.ext import commands

# Modules
from utils.logging import log_error
from views.verify_view import VerifyView
from webserver import close_webserver
from http_services import http_services

# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

class Class_bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        # Start HTTP session
        try:
            await http_services.ensure_http()
        except Exception as e:
            log_error(None, "Class_bot", 1, e)

        # Register perminant view
        self.add_view(VerifyView())

    async def on_ready(self):
        try:
            await self.tree.sync()
            print(f"[SETUP] COMPLETE - Bot Online: {self.user}")

        except Exception as e:
            log_error(None, "Class_bot", 2, e)

    async def close(self):
        await http_services.close()
        await close_webserver()
        await super().close()

    async def load_modules(self, context):
        for file in os.listdir("./bot/modules"):
            if file.endswith(".py"):
                module_name = f"bot.modules.{file[:-3]}"
                module = importlib.import_module(module_name)

                if hasattr(module, "setup"):
                    await module.setup(self, context)