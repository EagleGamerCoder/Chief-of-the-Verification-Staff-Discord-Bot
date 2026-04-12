'''

info

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import asyncio
import time

# Modules


# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

class SafetyManager:
    def __init__(self):
        self.user_cooldowns = {}
        self.roblox_cache = {}
        self.role_lock = asyncio.Lock()

    def check_cooldown(self, user_id: int, cooldown: int = 10):
        now = time.time()

        if user_id in self.user_cooldowns:
            if now - self.user_cooldowns[user_id] < cooldown:
                return False

        self.user_cooldowns[user_id] = now
        return True

    def cache_roblox(self, username: str, roblox_id: int):
        self.roblox_cache[username.lower()] = roblox_id

    def get_cached_roblox(self, username: str):
        return self.roblox_cache.get(username.lower())

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

safety = SafetyManager()