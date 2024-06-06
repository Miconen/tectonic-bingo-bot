from typing import Dict
import discord

from models.team import Team


def in_team(user: discord.Member, teams: Dict[int, Team]):
    """Returns the Discord role id of a team."""
    team_ids = teams.keys()

    for role in user.roles:
        if role.id in team_ids:
            return role.id
