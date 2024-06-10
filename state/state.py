import os
from typing import List, Dict
import jsonpickle

from models.team import Team

class State(object):
    teams: Dict[int, Team]
    tile_info: List[str]

    def __init__(self):
        self.teams = {}
        self.tile_info = []

    def get_team(self, team_id: int):
        """Get a team by ID."""
        return self.teams.get(team_id)

    def add_team(self, team: Team):
        """Add a team to the state."""
        self.teams.setdefault(team.get_id(), team)

    def remove_team(self, team_id: int):
        """Remove a team from the state."""
        self.teams.pop(team_id)

    def serialize(self):
        """Serialize the state to a JSON file."""
        try:
            path = os.getenv("STATE_PATH")
            if not path:
                raise Exception("No state path provided in environment variables.")

            with open(path, "w") as f:
                data = jsonpickle.encode(self, keys=True)
                if data is None:
                    raise Exception("Failed to serialize state")
                f.write(data)
                print("State serialized to JSON file successfully")
        except Exception as e:
            print("An error occurred while trying to serialize state. Exiting...")
            raise(e)

    @staticmethod
    def deserialize():
        """Deserialize the state from a JSON file."""
        s = None
        try:
            path = os.getenv("STATE_PATH")
            if not path:
                raise Exception("No state path provided in environment variables.")

            print("Attempting to load state from JSON file...")
            with open(path, "r") as f:
                s = jsonpickle.decode(f.read(), keys=True)
                print("State deserialized successfully")
        except FileNotFoundError:
            print("No JSON state file found, initializing state...")

            path = os.getenv("STATE_PATH")
            if not path:
                raise Exception("No state path provided in environment variables.")

            with open(path, "w") as f:
                data = jsonpickle.encode(State(), keys=True)
                if data is None:
                    raise Exception("Failed to initialize state")
                f.write(data)
                print("State initialized to JSON file successfully")
        except Exception as e:
            print("An error occurred while trying to load state. Exiting...")
            raise(e)

        if not isinstance(s, State):
            raise Exception("State is not an instance of State")

        return s


state = State.deserialize()
