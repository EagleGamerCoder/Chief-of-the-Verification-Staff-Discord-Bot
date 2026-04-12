'''

info

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports


# Modules
from http_services import http_services

# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

http_session = None

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# Get the roblox id of a user using their username
async def get_roblox_id(username : str) -> int | None:
    await http_services.ensure_http()
    async with http_services.http_session.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames" : [username]}, 
        timeout=10
    ) as response:
        try:
            data = await response.json()
        except Exception:
            return 0
        if data.get("data"):
            return data["data"][0]["id"]
    return None



# Get the profile description of a user using their roblox id
async def get_profile_description(user_id : int):
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10) as response:
        try:
            data = await response.json()
        except Exception:
            return 0
        return data.get("description", "")
        


# Get the group rank of a user using their roblox user id and group id
async def get_group_rank(user_id : int, group_id : int) -> int:
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles", timeout=10) as response:
        try:
            data = await response.json()
        except Exception:
            return 0

        for group in data.get("data", []):
            if group["group"]["id"] == group_id:
                return group["role"]["rank"]
    return 0



async def get_roblox_username(roblox_user_id : int) -> str:
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://users.roblox.com/v1/users/{roblox_user_id}", timeout=10) as response:
        try:
            data = await response.json()
        except Exception:
            return ""
        return data.get("name", "Unknown")



async def fetch_group_data(group_id):
    await http_services.ensure_http()
    async with http_services.http_session.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=10) as response:
        try:
            data = await response.json()
        except Exception:
            return 0
        return data
            
    return None