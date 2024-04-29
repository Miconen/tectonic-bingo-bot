from typing import Dict
from state.state import Team


def in_team(user_id: int, teams: Dict[int, Team]):
    # Get teams[team].name that the user belongs in
    for team in teams.values():
        for member in team.role.members:
            if user_id != member.id:
                continue

            return team.role.id
