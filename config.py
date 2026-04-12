'''

Info 

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import os 

# Modules
from dotenv import load_dotenv

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

print("[SETUP] Loading .env variables...")

# Load Environmental Variables 
load_dotenv()

# Get .Env Variables
discord_token = os.getenv('DISCORD_TOKEN')
if discord_token:
    print(f"[SETUP] discord_token: {bool(discord_token)}")
else:
    raise RuntimeError("discord_token is missing from .env variables")

main_guild_id = os.getenv('MAIN_GUILD_ID')
if main_guild_id:
    main_guild_id = int(main_guild_id)
    print(f"[SETUP] main_guild_id: {bool(main_guild_id)}")
else:
    raise RuntimeError("main_guild_id is missing from .env variables")

print(f"[SETUP] Loaded all .env variables!")