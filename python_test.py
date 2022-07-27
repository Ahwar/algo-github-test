from imaplib import Commands
import json
from queue import PriorityQueue
import random


def get_parse_commands(data: dict) -> list:
    """Get all the parse commands

    returns all the parse commands
    arguments:
        data: the dictionary containing data
    return:
        parse_commands: list of parse commands
    """

    parse_commands = [
        row for row in data if "function" in row and row["function"] == "parse"
    ]
    return parse_commands


def get_copy_commands(data: dict) -> list:
    """Get all the copy commands

    returns all the copy commands
    arguments:
        data: the dictionary containing data
    return:
        copy_commands: list of copy commands
    """

    copy_commands = [
        row for row in data if "function" in row and row["function"] == "copy"
    ]
    return copy_commands


def get_bad_commands(data: dict) -> int:
    """Get all the bad commands

    returns all the bad commands
    arguments:
        data: the dictionary containing data
    return:
        bad_commands: list of bad commands
    """

    bad_commands = [
        row for row in data if "function" in row and row["function"] == "bad value"
    ]
    bad_commands.append(
        [row for row in data if "value" in row and row["value"] == "bad value"]
    )
    return bad_commands


def main() -> (dict, dict, dict, dict, dict):
    # NOTE: Get all the parse commands
    with open("data.txt", "r") as file:
        data = json.loads(file.read())
    parse_commands = get_parse_commands(data=data)
    print(f"parse_commands: {parse_commands}")

    # NOTE: Get all the copy commands
    with open("data.txt", "r") as file:
        data = json.loads(file.read())
    copy_commands = get_copy_commands(data=data)
    print(f"copy_commands: {copy_commands}")

    # NOTE: Put the two lists together and say which list it came from as well as the item number for that list
    functional_commands = []
    
    def get_functional_commands(dict: dict, value: str):
        counter = 0
        for row in dict:
            counter += 1
            new_row = row.copy()
            new_row['_list'] = value
            new_row['_counter'] = counter
            functional_commands.append(new_row)

    get_functional_commands(parse_commands, 'parse')
    get_functional_commands(copy_commands, 'copy')
    print(f"functional_commands: {functional_commands}")
    # NOTE: Get random sampling of data
    random_commands = []
    with open("data.txt", "r") as file:
        data = json.loads(file.read())
        random_commands = random.sample(data, 2)
    print(f"random_commands: {random_commands}")

    # NOTE: Write the methodology to catch bad_commands
    bad_commands = list()
    bad_commands = get_bad_commands(data=data)
    return parse_commands, copy_commands, functional_commands, random_commands, bad_commands


if __name__ == '__main__':
    parse_commands, copy_commands, functional_commands, random_commands, bad_commands = main()

    assert parse_commands == [{'function': 'parse', 'help': 'file help', 'value': 'file'}]
    assert copy_commands == [{'function': 'copy', 'help': 'copy help', 'value': 'file'}]
    assert functional_commands == [{'function': 'parse', 'help': 'file help', 'value': 'file', '_list': 'parse', '_counter': 1}, {'function': 'copy', 'help': 'copy help', 'value': 'file', '_list': 'copy', '_counter': 1}]
    assert len(random_commands) == 2
    assert len(bad_commands) == 3
