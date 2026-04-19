'''

Module: reactions.py
Author: EagleGamerCoder
Most recent update version: V 0.5.4
Description:
    Tracks reactions made by the user to update the database.

Usage:
    _

Components:
    Functions:
        _

    Classes:
        _

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
        
        print("REACTION DETECTED")

        print("User:", payload.user_id)
        print("Guild:", payload.guild_id)
        print("Message:", payload.message_id)
        print("Emoji:", payload.emoji, str(payload.emoji))

        channel_id, message_id = db.get_server_rules_ids() 

        if payload.message_id != int(message_id):
            print("Wrong message")
            return

        if payload.emoji.name != "✅":
            print("Wrong emoji")
            return

        print("Saving to DB")
        db.save_accepted_rules(payload.guild_id, payload.user_id)

        print("Immediate check:",
            db.has_accepted_rules(payload.guild_id, payload.user_id))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Ignore bot
        if payload.user_id == self.bot.user.id:
            return

        # Same as before
        channel_id, message_id = db.get_server_rules_ids() 

        if payload.message_id != int(message_id):
            return

        if str(payload.emoji) != "✅":
            return

        db.remove_accepted_rules(payload.guild_id, payload.user_id)