'''

Module: verify_view.py
Author: EagleGamerCoder
Most recent update version: V 0.4.2
Description:
    Handles the Discord verification UI system, including
    persistent buttons and a modal used to collect Roblox
    usernames and complete role verification.

Usage:
    main.py
    bot.py

Components:
    Functions:
        get_guild_config(guild_id) -> dict | None

    Classes:
        UsernameModal
            on_submit

        StartVerificationButton
            __init__
            callback

        CompleteVerificationButton
            __init__
            callback

        UpdateButton
            __init__
            callback

        VerifyView
            __init__

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord
import time
import asyncio

# Modules
import db

from utils.safety import safety
from utils.general_funcs import generate_code_six
from utils.logging import log_error
from services import *

# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

BUTTON_COOLDOWN = 5 # in seconds
EXPIRY_TIME = 600 #(10 minutes = 600 seconds)

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def get_guild_config(guild_id : int) -> dict | None:
    config = db.get_guild_config(guild_id)
    if not config:
        return None
    try:
        channel_id, role_id, group_id, sub_one, sub_two, sub_three = config
        return {
            "channel_id" : channel_id,
            "role_id" : role_id,
            "group_id" : group_id,
            "sub_one" : sub_one,
            "sub_two" : sub_two,
            "sub_three" : sub_three,
        }
    except Exception:
        return None

# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

# Creates a modal to get a players username and begin the verification process
class UsernameModal(discord.ui.Modal, title="Enter Roblox Username"):
    username_ = discord.ui.TextInput(label="Roblox Username")

    async def on_submit(self, interaction : discord.Interaction):
        username = self.username_.value.strip()
        
        roblox_id = safety.get_cached_roblox(username)

        if roblox_id is None:
            #roblox_id = await get_roblox_id(username)
            safety.cache_roblox(username, roblox_id)

        if roblox_id is None:
            await interaction.response.send_message(
                "Username not found. Try again.", 
                ephemeral=True,
            )
            return
        
        code = generate_code_six()
        db.save_pending(
            discord_id=interaction.user.id, 
            roblox_id=roblox_id, 
            code=code, 
            created_at=int(time.time())
        )

        await interaction.response.send_message(
            f"Put this code into your Roblox bio:\n\n**{code}**\n\nThen press **Complete Verification**",
            ephemeral=True,
        )



# Creates a button that is used to begin verify users and connect to the modal.
class StartVerificationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Start Verification",
            style=discord.ButtonStyle.blurple,
            custom_id="persistent_start_verification"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if not safety.check_cooldown(interaction.user.id, BUTTON_COOLDOWN):
                await interaction.response.send_message(
                    f"⏳ Please wait {BUTTON_COOLDOWN} seconds before trying again.",
                    ephemeral=True
                )
                return

            ids = db.get_server_rules_ids(interaction.guild.id)
            if ids is None:
                await interaction.response.send_message(
                    "Server is not configured.",
                    ephemeral=True
                )
                log_error(interaction, "StartVerificationButton", 1, "Guild not configured")
                return

            if not db.has_accepted_rules(interaction.guild.id, interaction.user.id):
                await interaction.response.send_message(
                    "You must accept the rules first by reacting with '✅'.",
                    ephemeral=True
                )
                return

            await interaction.response.send_modal(UsernameModal())

        except Exception as e:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "An unexpected error occurred.",
                    ephemeral=True
                )
            await log_error(interaction, "StartVerificationButton", 2, e)



# Creates a button that is used to complete the verificiation process and save users data to the database (db), and finally auto-update their roles using services/role_sync.py.
class CompleteVerificationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Complete Verification",
            style=discord.ButtonStyle.green,
            custom_id="persistent_complete_verification"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if not safety.check_cooldown(interaction.user.id, BUTTON_COOLDOWN):
                await interaction.response.send_message(
                    f"⏳ Please wait {BUTTON_COOLDOWN} seconds before trying again.",
                    ephemeral=True
                )
                return

            await interaction.response.defer(ephemeral=True)

            pending = db.get_pending(interaction.user.id)
            if not pending:
                await interaction.followup.send("❌ Start Verification first.", ephemeral=True)
                return
            roblox_id, code, created_at = pending

            # Expiry check 
            if time.time() - created_at > EXPIRY_TIME:
                db.delete_pending(interaction.user.id)
                await interaction.followup.send("❌ Verification expired. Start again.", ephemeral=True)
                return
            
            config = get_guild_config(interaction.guild.id)
            if not config:
                log_error(interaction, "CompleteVerificationButton", 1, "Guild not configured")
                return
            '''
            description = await get_profile_description(roblox_id)
            if not description or code not in description:
                await interaction.followup.send("❌ Code not in bio.", ephemeral=True)
                return
            
            await asyncio.sleep(0.5)
            '''
            try:
                async with safety.role_lock:
                    '''
                    result = await sync_discord_roles(
                        interaction.user, 
                        interaction, 
                        int(config["group_id"]), 
                        int(config["sub_one"]), 
                        int(config["sub_two"]), 
                        int(config["sub_three"]),
                    )
                    '''

                #if result == 1:
                    role = interaction.guild.get_role(config["role_id"])
                    if role:
                        await interaction.user.add_roles(role) # adds verified role

                    db.save_verify(interaction.user.id, roblox_id)  
                    db.delete_pending(interaction.user.id)

                    await interaction.followup.send("✅ Verified!", ephemeral=True)
                #else:
                    await interaction.followup.send("❌ Verification Failed.", ephemeral=True)
                    return
                
            except Exception as e:
                await log_error(interaction, "CompleteVerificationButton", 2, e)

        except Exception as e:
            await log_error(interaction, "CompleteVerificationButton", 3, e)
        
        

# Creates a button that is used to update verified users' roles using services/role_sync.py.
class UpdateButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Update",
            style=discord.ButtonStyle.green,
            custom_id="persistent_update_verification",
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if not safety.check_cooldown(interaction.user.id, BUTTON_COOLDOWN):
                await interaction.response.send_message(
                    f"⏳ Please wait {BUTTON_COOLDOWN} seconds before trying again.",
                    ephemeral=True
                )
                return
            
            await interaction.response.defer(ephemeral=True)

            if not db.get_roblox_id(interaction.user.id):
                await interaction.followup.send("❌ Your account is not verified.", ephemeral=True)
                return
            
            config = get_guild_config(interaction.guild.id)
            if not config:
                log_error(interaction, "UpdateButton", 1, "Guild not configured")
                return

            await asyncio.sleep(0.5)
            
            try:
                async with safety.role_lock:
                    '''
                    result = await sync_discord_roles(
                        interaction.user, 
                        interaction, 
                        int(config["group_id"]), 
                        int(config["sub_one"]), 
                        int(config["sub_two"]), 
                        int(config["sub_three"]),
                    )
                    '''
                if result == 1:
                    return await interaction.followup.send("✅ Roles updated!", ephemeral=True)
                
                await interaction.followup.send("❌ Roles not updated.", ephemeral=True)
                
            except Exception as e:
                await log_error(interaction, "UpdateButton", 1, e)
                return
            
        except Exception as e:
            await log_error(interaction, "UpdateButton", 2, e)
        
        

# Persistent view that keeps buttons active across restarts (requires bot.add_view on startup). 
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent
        self.add_item(StartVerificationButton())
        self.add_item(CompleteVerificationButton())
        self.add_item(UpdateButton())