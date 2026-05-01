'''

Module: db.py
Author: EagleGamerCoder
Most recent update version: V 0.6.5
Description:
    Handles all database quieries including checking, getting 
    and saving.

Usage:
    verify_view.py
    reactions.py
    discord_roblox_role_sync.py

Components:
    Functions:
        init_database()
        set_guild_config(guild_id, channel_id, role_id, group_id, sub_group_id_one, sub_group_id_two, sub_group_id_three)
        get_guild_config(guild_id)
        save_pending(discord_id, roblox_id, code, created_at)
        get_pending(discord_id)
        delete_pending(discord_id)
        save_verify(discord_id, roblox_id)
        get_roblox_id(discord_id)
        save_server_rules_ids(guild_id, channel_id, message_id)
        get_server_rules_ids(guild_id)
        save_accepted_rules(guild_id, user_id)
        has_accepted_rules(guild_id, user_id)
        remove_accepted_rules(guild_id, user_id)

    Classes:
        _

 
'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import psycopg2
import os

# Modules


# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------



# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_database():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id BIGINT PRIMARY KEY,
        channel_id BIGINT,
        role_id BIGINT,
        group_id BIGINT,
        sub_group_id_one BIGINT,
        sub_group_id_two BIGINT,
        sub_group_id_three BIGINT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS pending_verifications (
        discord_id BIGINT PRIMARY KEY,
        roblox_id BIGINT,
        code TEXT,
        created_at BIGINT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS verified (
        discord_id BIGINT PRIMARY KEY,
        roblox_id BIGINT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS server_rules_ids (
        guild_id BIGINT PRIMARY KEY,
        channel_id BIGINT,
        message_id BIGINT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS accepted_rules (
        guild_id BIGINT,
        user_id BIGINT,
        PRIMARY KEY (guild_id, user_id)
    )
    """)

    conn.commit()
    conn.close()

# ------------------------------------------------------------ GUILD CONFIG ------------------------------------------------------------

def set_guild_config(guild_id, channel_id, role_id, group_id, sub_one, sub_two, sub_three):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO guild_config VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (guild_id) DO UPDATE SET
        channel_id = EXCLUDED.channel_id,
        role_id = EXCLUDED.role_id,
        group_id = EXCLUDED.group_id,
        sub_group_id_one = EXCLUDED.sub_group_id_one,
        sub_group_id_two = EXCLUDED.sub_group_id_two,
        sub_group_id_three = EXCLUDED.sub_group_id_three
    """, (guild_id, channel_id, role_id, group_id, sub_one, sub_two, sub_three))

    conn.commit()
    conn.close()

def get_guild_config(guild_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT channel_id, role_id, group_id, sub_group_id_one, sub_group_id_two, sub_group_id_three
    FROM guild_config WHERE guild_id = %s
    """, (guild_id,))

    data = c.fetchone()
    conn.close()
    return data

# ------------------------------------------------------------ PENDING ------------------------------------------------------------

def save_pending(discord_id, roblox_id, code, created_at):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO pending_verifications VALUES (%s, %s, %s, %s)
    ON CONFLICT (discord_id) DO UPDATE SET
        roblox_id = EXCLUDED.roblox_id,
        code = EXCLUDED.code,
        created_at = EXCLUDED.created_at
    """, (discord_id, roblox_id, code, created_at))

    conn.commit()
    conn.close()

def get_pending(discord_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT roblox_id, code, created_at
    FROM pending_verifications WHERE discord_id = %s
    """, (discord_id,))

    data = c.fetchone()
    conn.close()
    return data

def delete_pending(discord_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    DELETE FROM pending_verifications WHERE discord_id = %s
    """, (discord_id,))

    conn.commit()
    conn.close()

# ------------------------------------------------------------ VERIFIED ------------------------------------------------------------

def save_verify(discord_id, roblox_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO verified VALUES (%s, %s)
    ON CONFLICT (discord_id) DO UPDATE SET
        roblox_id = EXCLUDED.roblox_id
    """, (discord_id, roblox_id))

    conn.commit()
    conn.close()

def get_roblox_id(discord_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT roblox_id FROM verified WHERE discord_id = %s
    """, (discord_id,))

    data = c.fetchone()
    conn.close()
    return data[0] if data else None  # ✅ FIXED

# ------------------------------------------------------------ RULES ------------------------------------------------------------

def save_server_rules_ids(guild_id, channel_id, message_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO server_rules_ids VALUES (%s, %s, %s)
    ON CONFLICT (guild_id) DO UPDATE SET
        channel_id = EXCLUDED.channel_id,
        message_id = EXCLUDED.message_id
    """, (guild_id, channel_id, message_id))

    conn.commit()
    conn.close()

def get_server_rules_ids(guild_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT channel_id, message_id
    FROM server_rules_ids WHERE guild_id = %s
    """, (guild_id,))

    data = c.fetchone()
    conn.close()
    return data

def save_accepted_rules(guild_id, user_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO accepted_rules VALUES (%s, %s)
    ON CONFLICT (guild_id, user_id) DO NOTHING
    """, (guild_id, user_id))

    conn.commit()
    conn.close()

def has_accepted_rules(guild_id, user_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT 1 FROM accepted_rules
    WHERE guild_id = %s AND user_id = %s
    """, (guild_id, user_id))

    data = c.fetchone()
    conn.close()
    return data is not None

def remove_accepted_rules(guild_id, user_id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    DELETE FROM accepted_rules WHERE guild_id = %s AND user_id = %s
    """, (guild_id, user_id))

    conn.commit()
    conn.close()