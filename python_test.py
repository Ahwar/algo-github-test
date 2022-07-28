import json
import random

def read_file(file_name: str) -> dict:
    """
    return json in file as python dictionary

    arguments:
        file_name: the file which contains json data
    return:
        data: dictionary containing json data
    """
    with open(file_name, "r") as file:
        data = json.loads(file.read())
    return data

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

def get_functional_commands(dict: dict, value: str) -> list:
    """Get all the functional commands

    returns all the functional commands
    arguments:
        data: the dictionary containing data
    return:
        functional_commands: list of functional commands
    """
    
    counter, functional_commands = 0, []
    for row in dict:
        counter += 1
        new_row = row.copy()
        new_row['_list'] = value
        new_row['_counter'] = counter
        functional_commands.append(new_row)
    
    return functional_commands

def get_bad_commands(data: dict) -> list:
    """Get all the bad commands

    returns all the bad commands
    arguments:
        data: the dictionary containing data
    return:
        bad_commands: list of bad commands
    """

    bad_commands = [
        row
        for row in data
        if ("function" in row and row["function"] == "bad value")
        or ("value" in row and row["value"] == "bad value")
    ]
    return bad_commands



if __name__ == '__main__':

    data = read_file("data.txt")

    # NOTE: Get all the parse commands 
    parse_commands = get_parse_commands(data)
    print(f"parse_commands: {parse_commands}")

    # NOTE: Get all the copy commands
    copy_commands = get_copy_commands(data)
    print(f"copy_commands: {copy_commands}")

    # NOTE: Put the two lists together and say which list it came from as well as the item number for that list
    functional_commands = get_functional_commands(parse_commands, 'parse')
    functional_commands.append(get_functional_commands(copy_commands, 'copy')[0])
    print(f"functional_commands: {functional_commands}")

    # NOTE: Get random sampling of data
    random_commands = random.sample(data, 2)
    print(f"random_commands: {random_commands}")

    # NOTE: Write the methodology to catch bad_commands
    bad_commands = get_bad_commands(data)

    assert parse_commands == [{'function': 'parse', 'help': 'file help', 'value': 'file'}]
    assert copy_commands == [{'function': 'copy', 'help': 'copy help', 'value': 'file'}]
    assert functional_commands == [{'function': 'parse', 'help': 'file help', 'value': 'file', '_list': 'parse', '_counter': 1}, {'function': 'copy', 'help': 'copy help', 'value': 'file', '_list': 'copy', '_counter': 1}]
    assert len(random_commands) == 2
    assert len(bad_commands) == 3
