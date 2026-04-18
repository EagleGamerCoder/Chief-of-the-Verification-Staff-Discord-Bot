'''

Module: role_sync.py
Author: EagleGamerCoder
Most recent update version: V 0.4.2
Description:
    Manages adding roblox group roles and nicknames to 
    discord.

Usage:
    verify_view.py

Components:
    Functions:
        _

    Classes:
        _

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import discord
import asyncio
import re 

# Modules
import db
from config import main_guild_id
from utils.logging import log_error
from http_services  import http_services
from services import roblox_api

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def remove_leading_bracket(string : str) -> str:
    return re.sub(r'^\[.*?\]\s*','',string)



async def FetchRobloxGroupRole(discord_user_id: int, group_id):
    await http_services.ensure_http()
    
    # Fetches the Roblox group role for the specified group ID and interaction
    data = db.get_roblox_id(discord_user_id)
    if not data:
        return None

    roblox_user_id = data[0]

    if not roblox_user_id:
        return None

    # ---------------- FETCH GROUP DATA ----------------
    try:
        membership_url = f"https://groups.roblox.com/v1/users/{roblox_user_id}/groups/roles"

        async with http_services.http_session.get(membership_url, timeout=10) as response:

            if response.status == 404:
                return None

            data = await response.json()

        # ---------------- FIND TARGET GROUP ----------------
        for group in data.get("data", []):
            if group.get("group", {}).get("id") == group_id:
                return {
                    "name": group.get("role", {}).get("name", "Unknown"),
                    "id": group.get("role", {}).get("id", 0)
                }

        return None  # not in group

    except Exception as e:
        await log_error(None, "FetchRobloxGroupRole", 1, e)
        return None


'''
async def set_prefix_nickname(member, role_name: str):
    try: 
        match = re.match(r'^\[(.*?)\]', role_name)
        prefix = match.group(1) if match else ""

        if prefix != "":
            prefix = f"{prefix}]" 
        else:
            if role_name[:3] == "PRE": # Government rank
                prefix = "[PRESIDENT]"
            else:
                prefix = ""

        try:
            data = db.get_roblox_id(member.id)
            if data is not None:
                rblx_username = await get_roblox_username(data[0])
            else:
                rblx_username = "Unknown"

            await member.edit(nick=f"{prefix} {rblx_username}")

        except discord.Forbidden:
            await log_error(None, "set_prefix_nickname", 1, "Missing Permissions")
            return
        except discord.HTTPException as e:
            await log_error(None, "set_prefix_nickname", 2, e)
            return
            
    except Exception as e:
        await log_error(None, "set_prefix_nickname", 3, e)
        return
'''

'''
async def get_group_name_async(group_id):
    try:
        data = await fetch_group_data(group_id)
    except Exception:
        return None
    
    if data:
        return data.get("name")
    return None
'''

'''
async def get_roblox_multi_group_role(member : discord.member, interaction : discord.Interaction, group_id : int, sub_one : int, sub_two : int, sub_three : int):

    try:
        group_role = await FetchRobloxGroupRole(member.id, group_id)
        subgroup_name = None
    except Exception as e:
        await log_error(interaction, "get_roblox_multi_group_role", 1, e)
        return None, None

    # Collect subgroup ids that are non-zero in order of priority
    sub_ids = [sid for sid in (sub_one, sub_two, sub_three) if sid]
    if not sub_ids:
        return group_role, None

    fetch_tasks = [get_group_name_async(sid) for sid in sub_ids]
    names = await asyncio.gather(*fetch_tasks, return_exceptions=True)

    # Normalize and compare; only re-resolve role if a match is found
    for sid, name in zip(sub_ids, names):
        if isinstance(name, Exception) or name is None:
            continue
        normalized = remove_leading_bracket(name)
        if group_role and normalized == group_role.get("name"):
            try:
                group_role = await FetchRobloxGroupRole(member.id, sid)
                subgroup_name = normalized
            except Exception as e:
                await log_error(interaction, "get_roblox_multi_group_role", 2, f"Error fetching subgroup role for {sid}: {e}")
            break
    
    return group_role, subgroup_name
'''


async def get_category_role():
    pass


async def add_roles_to_user(*args):
    pass


async def sync_discord_and_roblox_roles(member: discord.member, interaction : discord.Interaction, group_id : int, sub_one : int, sub_two : int, sub_three : int) -> int | None:
    
    # Bot permission checks
    
    bot_member = interaction.guild.me

    if not bot_member.guild_permissions.manage_roles:
        await log_error(interaction, "sync_discord_roles", 1, "Missing Manage roles permission")
        return

    if not bot_member.guild_permissions.manage_nicknames:
        await log_error(interaction, "sync_discord_roles", 2, "Missing Change nicknames permission")
        return
    
    # Fetch role

    rank = roblox_api.get_group_rank(db.get_roblox_id(member.id)[0], group_id)
    data = roblox_api.get_group_data(group_id)

'''
async def sync_discord_roles(member: discord.Member, interaction: discord.Interaction, group_id : int, sub_one : int, sub_two : int, sub_three : int):

    bot_member = interaction.guild.me

    if not bot_member.guild_permissions.manage_roles:
        await log_error(interaction, "sync_discord_roles", 1, "Missing Manage roles permission")
        return

    if not bot_member.guild_permissions.manage_nicknames:
        await log_error(interaction, "sync_discord_roles", 2, "Missing Change nicknames permission")
        return

    # ---------------- FETCH ROLE ----------------
    
    group_role, subgroup_name = await get_roblox_multi_group_role(member, interaction, group_id, sub_one, sub_two, sub_three)

    # ---------------- HELPERS / CONFIG ----------------
    def normalize(name: str) -> str:
        if name is None:
            return ""
        return name.strip().upper()

    # Category role names in the guild
    CATEGORY_ROLE_NAMES = {
        "ENLISTED": "Enlisted",
        "OFFICER": "Officer",
        "CHIEF_OF_STAFF_BOARD": "👑 Chief of Staff Board",
        "DEVELOPER": "[DEV] Developer",
    }

    # Prefix groups (normalized)
    ENLISTED_PREFIX = ("[OR-",)
    OFFICER_PREFIX = ("[OF-",)
    CSB_PREFIXES = ("[CDS", "[VCD", "[SEA", "[CAS", "[VCA", "[ASM")
    DEV_PREFIX = ("[DEV",)

    # ---------------- WHEN USER HAS A ROBLOX GROUP ROLE ----------------
    if group_role:
        role_name = group_role.get("name", "Unknown")
        clean_name = normalize(role_name)

        keep_role_names = {interaction.guild.default_role.name, "Roblox Verified"}

        # Find the exact discord role that matches the Roblox role name
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role:
            keep_role_names.add(role.name)

        if not role:
            # Try a normalized lookup (in case of spacing/casing differences)
            role = discord.utils.find(
                lambda r: r.name.lower() == role_name.lower(),
                interaction.guild.roles
            )

        if not role:
            await log_error(interaction, "sync_discord_roles", 3, f"The {role_name} discord role does not exist.")
            return

        # Determine the new category for this role
        new_category_name = None
        if subgroup_name:
            new_category_name = subgroup_name
        else:
            if interaction.guild.id == main_guild_id or any(clean_name.startswith(p) for p in CSB_PREFIXES):
                if any(clean_name.startswith(p) for p in ENLISTED_PREFIX):
                    new_category_name = CATEGORY_ROLE_NAMES["ENLISTED"]
                elif any(clean_name.startswith(p) for p in OFFICER_PREFIX):
                    new_category_name = CATEGORY_ROLE_NAMES["OFFICER"]
                elif any(clean_name.startswith(p) for p in CSB_PREFIXES):
                    new_category_name = CATEGORY_ROLE_NAMES["CHIEF_OF_STAFF_BOARD"]
                elif any(clean_name.startswith(p) for p in DEV_PREFIX):
                    new_category_name = CATEGORY_ROLE_NAMES["DEVELOPER"]
            else:
                new_category_name = "HQ"

        # Resolve category role object (may be None if not configured)
        category_role = None
        if new_category_name:
            try:
                category_role = discord.utils.get(interaction.guild.roles, name=new_category_name)
            except Exception as e:
                await log_error(interaction, "sync_discord_roles", 4, f"The {new_category_name} discord role does not exist. Error Msg: {e}")

        # Build sets of roles to keep and to remove
        default_role = interaction.guild.default_role
        
        # Keep the main rank role and the new category role (if present)
        keep_role_names.add(role.name)
        if category_role:
            keep_role_names.add(category_role.name)

        # Identify current category roles on the member (so we can remove ones that don't match)
        current_category_roles = [
            r for r in member.roles
            if r.name in set(CATEGORY_ROLE_NAMES.values())
        ]

        # Roles to remove:
        # - Any role that is not @everyone, not Roblox Verified, not managed,
        #   not above the bot, and not in keep_role_names.
        to_remove = [
            r for r in member.roles
            if (
                r != default_role
                and r.name not in keep_role_names
                and not r.managed
                and r < interaction.guild.me.top_role
            )
        ]

        # Additionally, remove category roles that conflict with the new category.
        # Example: moving from Officer -> Chief of Staff Board should remove Officer role.
        conflicting_category_roles = [
            r for r in current_category_roles
            if r.name not in keep_role_names  # remove category roles that are not the new one
            and r < interaction.guild.me.top_role
        ]

        # Merge lists and deduplicate
        remove_set = {r for r in to_remove + conflicting_category_roles}

        # Perform removals (if any)
        if remove_set:
            try:
                await member.remove_roles(*remove_set, reason="Syncing Roblox rank")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 5, f"Failed to remove roles for {member.id}. Error Msg: {e}")

        # Add the main role if missing
        if role not in member.roles:
            try:
                await member.add_roles(role, reason="Syncing Roblox rank")
            except discord.Forbidden:
                await log_error(interaction, "sync_discord_roles", 6, f"Permission denied when adding role {role.name} to {member.id}")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 7, f"Failed to add role {role.name} to {member.id}. Error Msg: {e}")

        # Ensure category role is correct: remove other category roles (defensive) then add the new one
        # Remove any remaining category roles that are not the desired one
        remaining_conflicting = [
            r for r in member.roles
            if r.name in set(CATEGORY_ROLE_NAMES.values())
            and r.name != (category_role.name if category_role else None)
            and r < interaction.guild.me.top_role
        ]
        if remaining_conflicting:
            try:
                await member.remove_roles(*remaining_conflicting, reason="Syncing category roles")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 8, f"Failed to remove conflicting category roles for {member.id}. Error Msg: {e}")

        # Add the category role if applicable and missing
        if category_role and category_role not in member.roles:
            try:
                await member.add_roles(category_role, reason="Syncing category role")
            except discord.Forbidden:
                await log_error(interaction, "sync_discord_roles", 9, f"Permission denied when adding category role {category_role.name} to {member.id}")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 10, f"Failed to add category role {category_role.name} to {member.id}. Error Msg: {e}")

        # Nickname update
        try:
            await set_prefix_nickname(member, role_name)
        except Exception as e:
            await log_error(interaction, "sync_discord_roles", 11, f"Failed to set nickname for {member.id}. Error Msg: {e}")

        # DM the user (best-effort)
        try:
            await member.send(f"You have been ranked in 'Calderian Army' to the '**{role.name}**' rank.")
        except discord.Forbidden:
            pass

        return 1
    
    # ---------------- WHEN USER HAS NO ROBLOX GROUP ROLE ----------------
    else:
        # Remove all non-exempt roles (we will keep category roles only if desired)
        default_role = interaction.guild.default_role
        roles_to_strip = [
            r for r in member.roles
            if (
                r.name not in ["Roblox Verified", default_role.name]
                and not r.managed
                and r < interaction.guild.me.top_role
            )
        ]
        if roles_to_strip:
            try:
                await member.remove_roles(*roles_to_strip, reason="User not in Roblox group")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 12, f"Failed to strip roles for {member.id}. Error Msg: {e}")

        civilian_role = discord.utils.get(interaction.guild.roles, name="[CIV] Civilian")
        if civilian_role and civilian_role not in member.roles:
            try:
                await member.add_roles(civilian_role, reason="Assign civilian role")
            except discord.Forbidden:
                await log_error(interaction, "sync_discord_roles", 13, f"Permission denied when adding civilian role to {member.id}")
            except discord.HTTPException as e:
                await log_error(interaction, "sync_discord_roles", 14, f"Failed to add civilian role to {member.id}. Error Msg: {e}")

        try:
            await member.send(
                f"You have been ranked in the {interaction.guild.name} Discord Server\n"
                "You are not in the Roblox group. You have been given the role: **Civilian**."
            )
        except discord.Forbidden:
            pass

        return 1
'''