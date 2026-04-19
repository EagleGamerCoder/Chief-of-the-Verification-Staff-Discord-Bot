'''

Module: data_loader.py
Author: EagleGamerCoder
Most recent update version: V 0.6.1
Description:
    Controls the data and json files. 

Usage:
    commands.py

Components:
    Functions:
        load_data()
        save_data(data)
        get_branch(branch_name: str)
        update_branch_field(branch_name: str, field: str, value: str)
        update_sub_branch(branch, sub, field, value)
        add_sub_branch(branch, sub_key, name, description, roblox)
        remove_sub_branch(branch, sub_key)

    Classes:
        _

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import json

# Modules


# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

BRANCH_FILE_PATH="data/branch_info.json"

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

def load_data():
    with open(BRANCH_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(BRANCH_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_branch(branch_name: str):
    data = load_data()
    return data.get(branch_name)


def update_branch_field(branch_name: str, field: str, value: str):
    data = load_data()

    if branch_name not in data:
        return False

    data[branch_name][field] = value
    save_data(data)
    return True

def update_sub_branch(branch, sub, field, value):
    data = load_data()

    if branch not in data:
        return False

    if sub not in data[branch]["sub_branches"]:
        return False

    data[branch]["sub_branches"][sub][field] = value
    save_data(data)
    return True

def add_sub_branch(branch, sub_key, name, description, roblox):
    data = load_data()

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


def remove_sub_branch(branch, sub_key):
    data = load_data()

    if branch not in data:
        return False

    if sub_key not in data[branch].get("sub_branches", {}):
        return False

    del data[branch]["sub_branches"][sub_key]

    save_data(data)
    return True