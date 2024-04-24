from typing import List
from state.state import Team

def in_team(user_id: str, teams: List[Team]):
    for team in teams:
        if user_id in team.members:
            return team.name
