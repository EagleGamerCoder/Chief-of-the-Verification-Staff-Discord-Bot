'''

Module: data_loader.py
Author: EagleGamerCoder
Most recent update version: V 0.6.3
Description:
    Controls the data and json files. 

Usage:
    commands.py

Components:
    Functions:
        load_data(file_path : str)
        save_data(data, file_path : str)

        BRANCH_get_branch(branch_name: str)
        BRANCH_update_branch_field(branch_name: str, field: str, value: str)
        BRANCH_update_sub_branch(branch, sub, field, value)
        BRANCH_add_sub_branch(branch, sub_key, name, description, roblox)
        BRANCH_remove_sub_branch(branch, sub_key)
        
        RANK_change_rank_holder(rank, new_holder)

    Classes:
        _

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import json

# Modules


# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

BRANCH_FILE_PATH="data/branch_info.json"
RANK_FILE_PATH="data/rank_info.json"
RANK_LIST_FILE_PATH="data/rank_list.json"

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

# -------------------- GENERAL FUNCS --------------------

def load_data(file_path : str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data, file_path : str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# -------------------- BRANCH FUNCS --------------------

def BRANCH_get_branch(branch_name: str):
    data = load_data(BRANCH_FILE_PATH)
    return data.get(branch_name)

def BRANCH_update_branch_field(branch_name: str, field: str, value: str):
    data = load_data(BRANCH_FILE_PATH)

    if branch_name not in data:
        return False

    data[branch_name][field] = value
    save_data(data, BRANCH_FILE_PATH)
    return True

def BRANCH_update_sub_branch(branch, sub, field, value):
    data = load_data(BRANCH_FILE_PATH)

    if branch not in data:
        return False

    if sub not in data[branch]["sub_branches"]:
        return False

    data[branch]["sub_branches"][sub][field] = value
    save_data(data, BRANCH_FILE_PATH)
    return True

def BRANCH_add_sub_branch(branch, sub_key, name, description, roblox):
    data = load_data(BRANCH_FILE_PATH)

    if branch not in data:
        return False

    if "sub_branches" not in data[branch]:
        data[branch]["sub_branches"] = {}

    data[branch]["sub_branches"][sub_key] = {
        "name": name,
        "description": description,
        "roblox": roblox
    }

    save_data(data)
    return True


def BRANCH_remove_sub_branch(branch, sub_key):
    data = load_data(BRANCH_FILE_PATH)

    if branch not in data:
        return False

    if sub_key not in data[branch].get("sub_branches", {}):
        return False

    del data[branch]["sub_branches"][sub_key]

    save_data(data, BRANCH_FILE_PATH)
    return True

# -------------------- RANK FUNCS --------------------

def RANK_change_rank_holder(rank, new_holder, discord_id):
    data = load_data(RANK_FILE_PATH)

    found_key = None
    for key, value in data.items():
        if rank in value["ranks"]:
            found_key = key
            break

    if found_key is None:
        return False

    data[found_key]["ranks"][rank]["holder"] = new_holder
    data[found_key]["ranks"][rank]["discord_id"] = discord_id
    save_data(data, RANK_FILE_PATH)
    return True