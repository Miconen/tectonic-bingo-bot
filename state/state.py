from typing import List, Dict
import sys

import jsonpickle

from models.team import Team


class State(object):
    teams: Dict[int, Team]
    tile_info: List[str]

    def __init__(self):
        self.teams = {}
        self.tile_info = []

    def serialize(self):
        """Serialize the state to a JSON file."""
        try:
            with open("state.json", "w") as f:
                data = jsonpickle.encode(self)
                if data is None:
                    raise Exception("Failed to serialize state")
                f.write(data)
                print("State serialized to JSON file successfully")
        except Exception as e:
            print("An error occurred while trying to serialize state. Exiting...")
            sys.exit(1)

    @staticmethod
    def deserialize():
        """Deserialize the state from a JSON file."""
        s = None
        try:
            print("Attempting to load state from JSON file...")
            with open("state.json", "r") as f:
                s = jsonpickle.decode(f.read())
                print("State deserialized successfully")
        except FileNotFoundError:
            print("No JSON state file found, initializing state...")
            with open("state.json", "w") as f:
                data = jsonpickle.encode(State())
                if data is None:
                    raise Exception("Failed to initialize state")
                f.write(data)
                print("State initialized to JSON file successfully")
        except Exception as e:
            print("An error occurred while trying to load state. Exiting...")
            sys.exit(1)

        if not isinstance(s, State):
            raise Exception("State is not an instance of State")

        return s


state = State.deserialize()
