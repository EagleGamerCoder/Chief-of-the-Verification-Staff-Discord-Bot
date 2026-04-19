'''

Module: reactions.py
Author: EagleGamerCoder
Most recent update version: V 0.6.1
Description:
    Tracks reactions made by the user to update the database.

Usage:
    bot.py

Components:
    Functions:
        setup(bot, ctx)

    Classes:
        ReactionHandler(commands.Cog)
            __init__(self, bot)
            on_raw_reaction_add(self, payload)
            on_raw_reaction_remove(self, payload)

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
from discord.ext import commands

# Modules
import db

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Sets up the reaction handler tied to the bot
async def setup(bot, ctx):
    await bot.add_cog(ReactionHandler(bot))

# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

# Handles reactions made by all users 
class ReactionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # Ignore bot
        if payload.user_id == self.bot.user.id:
            return

        channel_id, message_id = db.get_server_rules_ids(payload.guild_id) 

        if payload.message_id != int(message_id):
            return

        if payload.emoji.name != "✅":
            return

        db.save_accepted_rules(payload.guild_id, payload.user_id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Ignore bot
        if payload.user_id == self.bot.user.id:
            return

        # Same as before
        channel_id, message_id = db.get_server_rules_ids(payload.guild_id) 

        if payload.message_id != int(message_id):
            return

        if str(payload.emoji) != "✅":
            return

        db.remove_accepted_rules(payload.guild_id, payload.user_id)