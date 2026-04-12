'''

info

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
from services.role_sync import sync_discord_roles
from services.roblox_api import (
    get_roblox_id,
    get_profile_description,
)

# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

# Creates a modal to get a players username and begin the verification process
class UsernameModal(discord.ui.Modal, title="Enter Roblox Username"):
    username_ = discord.ui.TextInput(label="Roblox Username")

    async def on_submit(self, interaction : discord.Interaction):
        username = self.username_.value
        
        roblox_id = safety.get_cached_roblox(username)

        if not roblox_id:
            roblox_id = await get_roblox_id(username)
            safety.cache_roblox(username, roblox_id)

        if not roblox_id:
            await interaction.response.send_message(
                "Username not found. Try again.", 
                ephemeral=True,
            )
            return
        
        code = generate_code_six()
        db.save_pending(discord_id=interaction.user.id, roblox_id=roblox_id, code=code, created_at=int(time.time()))

        await interaction.response.send_message(
            f"Put this code into your Roblox bio:\n\n**{code}**\n\nThen press **Complete Verification**",
            ephemeral=True,
        )



class StartVerificationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Start Verification",
            style=discord.ButtonStyle.blurple,
            custom_id="persistent_start_verification"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            if not safety.check_cooldown(interaction.user.id, 10):
                await interaction.response.send_message(
                    "⏳ Please wait before trying again.",
                    ephemeral=True
                )
                return

            ids = db.get_server_rules_ids(interaction.guild.id)
            if ids is None:
                log_error(interaction, "StartVerificationButton", 1, "Guild not configured")
                return

            channel_id, message_id = ids
            channel = interaction.guild.get_channel(channel_id)

            if not channel:
                await interaction.response.send_message("❌ Rules channel not found.", ephemeral=True)
                return

            # FAST DB CHECK
            if not db.has_accepted_rules(interaction.guild.id, interaction.user.id):
                await interaction.response.send_message(
                    "You must accept the rules first by reacting with '✅' in the rules channel.",
                    ephemeral=True
                )
                return

            # MODAL
            await interaction.response.send_modal(UsernameModal())

        except Exception as e:
            await log_error(interaction, "StartVerificationButton", 2, e)

class CompleteVerificationButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Complete Verification",
            style=discord.ButtonStyle.green,
            custom_id="persistent_complete_verification"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            
            if not safety.check_cooldown(interaction.user.id, 10):
                await interaction.followup.send(
                    "⏳ Please wait before trying again.",
                    ephemeral=True
                )
                return

            data = db.get_pending(interaction.user.id)
            if not data:
                await interaction.followup.send("❌ Start Verification first.", ephemeral=True)
                return
            roblox_id, code, created_at = data

            # Expiry check (10 minutes = 600 seconds)
            if time.time() - created_at > 600:
                db.delete_pending(interaction.user.id)
                await interaction.followup.send("❌ Verification expired. Start again.", ephemeral=True)
                return
            
            config = db.get_guild_config(interaction.guild.id)
            if not config:
                log_error(interaction, "CompleteVerificationButton", 1, "Guild not configured")
                return
            channel_id, role_id, group_id, sub_one, sub_two, sub_three = config
            
            description = await get_profile_description(roblox_id)
            if code not in description:
                await interaction.followup.send("❌ Code not in bio.", ephemeral=True)
                return
            
            await asyncio.sleep(0.5)

            try:
                async with safety.role_lock:
                    result = await sync_discord_roles(interaction.user, interaction, int(group_id), int(sub_one), int(sub_two), int(sub_three))
                if result == 1:
                    role = interaction.guild.get_role(role_id)
                    if role:
                        await interaction.user.add_roles(role) # adds verified role

                    db.save_verify(interaction.user.id, roblox_id)  
                    db.delete_pending(interaction.user.id)

                    await interaction.followup.send("✅ Verified!", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Error with Verification.", ephemeral=True)
                    return
            except Exception as e:
                await log_error(interaction, "CompleteVerificationButton", 2, e)

        except Exception as e:
            await log_error(interaction, "CompleteVerificationButton", 3, e)
        
        

class UpdateButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Update",
            style=discord.ButtonStyle.green,
            custom_id="persistent_update_verification",
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)

            if not safety.check_cooldown(interaction.user.id, 10):
                await interaction.followup.send(
                    "⏳ Please wait before trying again.",
                    ephemeral=True
                )
                return

            data = db.get_roblox_id(interaction.user.id)
            if data is None:
                await interaction.followup.send("❌ Your account is not verified.", ephemeral=True)
                return
            
            config = db.get_guild_config(interaction.guild.id)
            if not config:
                log_error(interaction, "UpdateButton", 1, "Guild not configured")
                return
            channel_id, role_id, group_id, sub_one, sub_two, sub_three = config

            await asyncio.sleep(0.5)
            
            try:
                async with safety.role_lock:
                    result = await sync_discord_roles(interaction.user, interaction, int(group_id), int(sub_one), int(sub_two), int(sub_three))
                if result == 1:
                    await interaction.followup.send("✅ Roles updated!", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Roles not updated.", ephemeral=True)
            except Exception as e:
                await log_error(interaction, "UpdateButton", 1, e)
                return
            
        except Exception as e:
            await log_error(interaction, "UpdateButton", 2, e)
        
        

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent
        self.add_item(StartVerificationButton())
        self.add_item(CompleteVerificationButton())
        self.add_item(UpdateButton())