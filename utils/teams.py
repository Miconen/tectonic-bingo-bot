from typing import Dict
from state.state import Team


def in_team(user_id: int, teams: Dict[str, Team]):
    # Get teams[team].name that the user belongs in
    for name, team in teams.items():
        if user_id in team.members:
            return name
