'''

Module: roblox_api.py
Author: EagleGamerCoder
Most recent update version: V 0.5.1
Description:
    Handles all connections to the roblox api using aiohttp.

Usage:
    discord_roblox_role_sync.py
    verify_view.py

Components:
    Functions:
        get_roblox_id(rblx_username : str) -> int | None
        get_roblox_player_data(rblx_user_id : int) -> int | any
        get_roblox_player_group_data(rblx_user_id : int, rblx_group_id : int) -> int | any
        get_roblox_group_info(rblx_group_id : int) -> any

    Classes:
        _

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports


# Modules
from http_services import http_services

# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

http_session = None
TIME_OUT = 10

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Get the roblox id of a user using their username
async def get_roblox_id(rblx_username : str) -> int | None:
    await http_services.ensure_http()
    async with http_services.http_session.post("https://users.roblox.com/v1/usernames/users", json={"usernames" : [rblx_username]}, timeout=TIME_OUT) as response:
        try:
            data = await response.json()
        except Exception:
            return 0
        if data.get("data"):
            return int(data["data"][0]["id"])
    return None



# Get the profile description of a user using their roblox id
async def get_roblox_player_data(rblx_user_id : int) -> int | any:
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://users.roblox.com/v1/users/{rblx_user_id}", timeout=TIME_OUT) as response:
        try:
            data = await response.json()
        except Exception:
            return 0
        return data
        


# Get the group rank of a user using their roblox user id and group id
async def get_roblox_player_group_data(rblx_user_id : int, rblx_group_id : int) -> int | any:
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://groups.roblox.com/v2/users/{rblx_user_id}/groups/roles", timeout=TIME_OUT) as response:
        try:
            data = await response.json()
        except Exception:
            return 0

        for group in data.get("data", []):
            if group["group"]["id"] == rblx_group_id:
                return group
    return 0



# Getys the group information of the specified roblox group id
async def get_roblox_group_info(rblx_group_id : int) -> any:
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://groups.roblox.com/v1/groups/{rblx_group_id}", timeout=TIME_OUT) as response:
        try:
            data = response.json()
        except Exception:
            return 0
        
        return data
    return 0