'''

Module: commands.py
Author: EagleGamerCoder
Most recent update version: V 0.6.4
Description:
    Controls all commmands that are avaliable by the bot.

Usage:
    bot.py

Components:
    Functions:
        get_branch_data()
        get_branches()
        get_sub_branches(branch)
        branch_autocomplete(interaction: discord.Interaction, current: str)
        sub_branch_autocomplete(interaction: discord.Interaction, current: str)
        setup(bot, context)
            on_app_commmand_error(interaction: discord.Interaction, error: app_commands.AppCommandError)
            setup_config(interaction : discord.Interaction, role : discord.Role,  group_id : int, sub_group_id_one : int, sub_group_id_two : int, sub_group_id_three : int)
            setup_embeds(interaction : discord.Interaction, server_rules_channel_id : str, server_rules_message_id : str | None)
            create_all_roles(interaction : discord.Interaction)
            send_branch_info(interaction : discord.Interaction)
            edit_branch_info(interaction : discord.Interaction, branch: str, field: str, value: str)
            add_sub_branch(interaction: discord.Interaction, branch: str, key: str, name: str, description: str, roblox: str)
            remove_sub_branch(interaction: discord.Interaction, branch: str, sub: str)
            send_rank_info(interaction : discord.Interaction)
            change_rank_holder(interaction : discord.Interaction, rank : str, rblx_username : str, discord_member : discord.Member)

    Classes:
        _


'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord
from discord import app_commands

# Modules
from utils import data_loader
from views import embeds
from services import roblox_api

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def get_branch_data():
    data = data_loader.load_data("data/branch_info.json")
    
    if not data or not isinstance(data, dict):
        return None
        
    return data

def get_branches():
    data = data_loader.load_data()
    return list(data.keys())


def get_sub_branches(branch):
    data = data_loader.load_data()
    if branch not in data:
        return []
    return list(data[branch].get("sub_branches", {}).keys())

async def branch_autocomplete(interaction: discord.Interaction, current: str):
    branches = get_branches()

    return [
        app_commands.Choice(name=b, value=b)
        for b in branches if current.lower() in b.lower()
    ][:25]

async def sub_branch_autocomplete(interaction: discord.Interaction, current: str):
    branch = None

    # try to read already typed branch
    options = interaction.data.get("options", [])
    for opt in options:
        if opt["name"] == "branch":
            branch = opt["value"]

    if not branch:
        return []

    subs = get_sub_branches(branch)

    return [
        app_commands.Choice(name=s, value=s)
        for s in subs if current.lower() in s.lower()
    ][:25]

async def setup(bot, context):
    # Catches command errors
    @bot.tree.error
    async def on_app_commmand_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        await context.log_error(interaction, "on_app_commmand_error", 1, error)

    # ------------------------- ADMIN COMMANDS -------------------------

    # /setup_config
    @bot.tree.command(name="setup-config", description="Sets up the config for the Bot (Use `/setup_embeds` first).")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_config(interaction : discord.Interaction, role : discord.Role,  group_id : int, sub_group_id_one : int, sub_group_id_two : int, sub_group_id_three : int):
        await interaction.response.defer(ephemeral=True)

        await interaction.followup.send("Setting up config...", ephemeral=True)

        server_rules_ids = context.db.get_server_rules_ids(interaction.guild.id)
        if not server_rules_ids:
            await interaction.followup.send("Server rules ids, Invalid, Run `/setup_embeds` first.", ephemeral=True)
            return

        try:
            context.db.set_guild_config(interaction.guild.id, interaction.channel.id, role.id, group_id, sub_group_id_one, sub_group_id_two, sub_group_id_three)

            await interaction.followup.send(
                "✅ Setup complete.", 
                ephemeral=True,
            )

        except Exception as e:
            await context.log_error(interaction, "setup_config", 1, e)
    


    # /setup_embeds
    @bot.tree.command(name="setup-embeds", description="Sets up the Server rules embed and the verification emded (Use in #Verification).")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_embeds(interaction : discord.Interaction, server_rules_channel_id : str):
        await interaction.response.defer(ephemeral=True)

        await interaction.followup.send("Setting up embeds...", ephemeral=True)

        # Validate channel
        try:
            server_rules_channel = interaction.guild.get_channel(int(server_rules_channel_id))
            if server_rules_channel is None:
                await interaction.followup.send("❌ Invalid channel ID.", ephemeral=True)
                return
        except:
            await interaction.followup.send("❌ Invalid channel ID format.", ephemeral=True)
            return

        try:
            
            msg = None

            # Delete old embeds if they exist
            async for i in interaction.channel.history(limit=100):
                if i.author.id == bot.user.id:
                    await i.delete()
            async for i in server_rules_channel.history(limit=100):
                if i.author.id == bot.user.id:
                    await i.delete()

            # Send rules embed
            await server_rules_channel.send("# __**Server Rules:**__")
            msg = await server_rules_channel.send(embed=context.create_server_rules_embed())
            await msg.add_reaction('✅')

            # Send verification embed
            await interaction.channel.send(f"# __**Welcome to the {interaction.guild.name} Discord Server!**__")
            await interaction.channel.send(embed=context.create_verification_embed(),view=context.VerifyView())

            # Final response
            await interaction.followup.send("✅ Setup complete.", ephemeral=True)
                
            if msg == None:
                return

            context.db.save_server_rules_ids(interaction.guild.id, server_rules_channel.id, msg.id)

        except Exception as e:
            await context.log_error(interaction, "setup_embeds", 3, e)
            return
    
    #/create_all_roles
    @bot.tree.command(name="create-all-roles", description="Creates all roles for the configured info.")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_all_roles(interaction : discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Creating all roles...", ephemeral=True)

        config = context.db.get_guild_config(interaction.guild.id)
        if not config:
            await interaction.followup.send("Guild not configured, run `/setup_config` first.", ephemeral=True)

        roblox_group_id = config.group_id

        group_info = roblox_api.get_roblox_group_info(roblox_group_id)

        print(group_info)

    # ------------------------- BRANCH INFO COMMANDS --------------------

    # /send_branch_info
    @bot.tree.command(name="send-branch-info", description="Sends the branch info")
    @app_commands.checks.has_permissions(administrator=True)
    async def send_branch_info(interaction : discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Sending branch info...", ephemeral=True)

        try:

            data = get_branch_data()

            async for msg in interaction.channel.history(limit=100):
                if msg.author.id == bot.user.id:
                    await msg.delete()

            if not data:
                await interaction.followup.send("Data not found.", ephemeral=True)
                return
            
            await interaction.channel.send("# __**Branch Information:**__")

            for name, b_data in data.items():
                embed = embeds.create_branch_info_embed(b_data)
                await interaction.channel.send(embed=embed)
            
            await interaction.followup.send("Branch info sent.", ephemeral=True)
        
        except Exception as e:
            await context.log_error(interaction, "send_branch_info", 1, e)

    # /edit_branch_info
    @bot.tree.command(name="edit-branch-info", description="Edits a specified branches info.")
    @app_commands.checks.has_permissions(administrator=True)
    async def edit_branch_info(interaction : discord.Interaction, branch: str, field: str, value: str):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Updating branch info...", ephemeral=True)

        success = data_loader.BRANCH_update_branch_field(branch, field, value)

        if not success:
            await interaction.response.send_message("Branch not found.", ephemeral=True)
            return

        data = data_loader.load_data()[branch]
        embed = embeds.create_branch_info_embed(branch, data)

        await interaction.channel.send(embed=embed)

        await interaction.followup.send("Updated branch info!", ephemeral=True)

    # /add_sub_branch
    @bot.tree.command(name="add-sub-branch", description="Adds a new sub branch.")
    @app_commands.autocomplete(branch=branch_autocomplete)
    @app_commands.checks.has_permissions(administrator=True)
    async def add_sub_branch(interaction: discord.Interaction, branch: str, key: str, name: str, description: str, roblox: str):

        interaction.response.defer(ephemeral=True)

        success = data_loader.BRANCH_add_sub_branch(branch, key, name, description, roblox)

        if not success:
            await interaction.followup.send("Invalid Branch.", ephemeral=True)
            return

        await interaction.followup.send(
            f"Sub-branch `{name}` added to `{branch}`",
            ephemeral=True
        )

    # /remove_sub_branch
    @bot.tree.command(name="remove-sub-branch", description="Removes a sub branch.")
    @app_commands.autocomplete(branch=branch_autocomplete,sub=sub_branch_autocomplete)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_sub_branch(interaction: discord.Interaction, branch: str, sub: str):

        interaction.response.defer(ephemeral=True)

        success = data_loader.BRANCH_remove_sub_branch(branch, sub)

        if not success:
            await interaction.followup.send("Invalid Branch.", ephemeral=True)
            return

        await interaction.followup.send(
            f"Removed `{sub}` from `{branch}`",
            ephemeral=True
        )
    
    # ------------------------- RANK INFO COMMANDS -------------------------

    #/send_rank_info
    @bot.tree.command(name="send-rank-info", description="Sends the rank info")
    @app_commands.checks.has_permissions(administrator=True)
    async def send_rank_info(interaction : discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Sending rank info...", ephemeral=True)

        try:

            data = data_loader.load_data("data/rank_info.json")

            async for msg in interaction.channel.history(limit=100):
                if msg.author.id == bot.user.id:
                    await msg.delete()

            if not data:
                await interaction.followup.send("Data not found.", ephemeral=True)
                return
            
            await interaction.channel.send("# __**Rank Information:**__")

            for name, r_data in data.items():
                embed = await embeds.create_rank_info_embed(interaction, r_data)
                await interaction.channel.send(embed=embed)
            
            await interaction.followup.send("Rank info sent.", ephemeral=True)
        
        except Exception as e:
            await context.log_error(interaction, "send_rank_info", 1, e)

    #/change_rank_holder
    @bot.tree.command(name="change-rank-holder", description="Changes the holder of a rank.")
    @app_commands.checks.has_permissions(administrator=True)
    async def change_rank_holder(interaction : discord.Interaction, rank : str, rblx_username : str, discord_member : discord.Member):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Updating rank holder...", ephemeral=True)

        try:

            rank_list = data_loader.load_data("data/rank_list.json")
            if rank not in rank_list:
                await interaction.followup.send("Rank not found.", ephemeral=True)
                return
            
            rank_name = rank_list[rank]

            success = data_loader.RANK_change_rank_holder(rank, rblx_username, discord_member.id)
            
            if not success:
                await interaction.followup.send("Invalid input.", ephemeral=True)
                return

            await interaction.followup.send(f"Updated {rblx_username} to {rank_name}, Run `/send_rank_info`", ephemeral=True)

        except Exception as e:
            await context.log_error(interaction, "change_rank_holder", 1, e)

    # ------------------------- LIMITED COMMANDS -------------------------

    # Commands here

    # ------------------------- REGULAR COMMANDS -------------------------

    # /ping
    @bot.tree.command(name="ping",description="Tests the bots response by responding with pong.")
    async def ping(interaction : discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Pong",ephemeral=True)