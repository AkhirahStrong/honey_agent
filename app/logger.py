# app/logger.py

import json


def log_event(event):
    """
    Saves one Honey Agent event to a log file.

    event should be a Python dictionary.
    """

    with open("honey_agent.log", "a") as log_file:
        json.dump(event, log_file)
        log_file.write("\n")