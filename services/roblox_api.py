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
from __future__ import annotations
from typing import Any, Optional
import aiohttp
import asyncio

# Modules
from http_services import http_services
# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

TIME_OUT = 10

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Get the roblox id of a user using their username
async def get_roblox_id(rblx_username: str) -> Optional[int]:
    await http_services.ensure_http()
    session: aiohttp.ClientSession = http_services.http_session

    try:
        async with session.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [rblx_username]},
            timeout=aiohttp.ClientTimeout(total=TIME_OUT)
        ) as response:
            response.raise_for_status()
            data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    items = data.get("data")
    if items:
        return int(items[0].get("id"))
    return None


# Get the profile data of a user using their roblox id
async def get_roblox_player_data(rblx_user_id: int) -> Optional[dict[str, Any]]:
    await http_services.ensure_http()
    session: aiohttp.ClientSession = http_services.http_session

    try:
        async with session.get(
            f"https://users.roblox.com/v1/users/{rblx_user_id}",
            timeout=aiohttp.ClientTimeout(total=TIME_OUT)
        ) as response:
            response.raise_for_status()
            data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    return data


# Get the group rank of a user using their roblox user id and group id
async def get_roblox_player_group_data(rblx_user_id: int, rblx_group_id: int) -> Optional[dict[str, Any]]:
    await http_services.ensure_http()
    session: aiohttp.ClientSession = http_services.http_session

    try:
        async with session.get(
            f"https://groups.roblox.com/v2/users/{rblx_user_id}/groups/roles",
            timeout=aiohttp.ClientTimeout(total=TIME_OUT)
        ) as response:
            response.raise_for_status()
            data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    for group in data.get("data", []):
        if group.get("group", {}).get("id") == rblx_group_id:
            return group
    return None


# Get the group information of the specified roblox group id
async def get_roblox_group_info(rblx_group_id: int) -> Optional[dict[str, Any]]:
    await http_services.ensure_http()
    session: aiohttp.ClientSession = http_services.http_session

    try:
        async with session.get(
            f"https://groups.roblox.com/v1/groups/{rblx_group_id}",
            timeout=aiohttp.ClientTimeout(total=TIME_OUT)
        ) as response:
            response.raise_for_status()
            data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

    return data