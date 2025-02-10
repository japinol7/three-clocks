"""Module experience points."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.models.actors.actor_types import ActorType


class ExperiencePoints:
    xp_points = {
        'game_level': 75,
        'beat_the_game': 150,
        ActorType.CLOCK_A.name: 250,
        ActorType.MINE_LILAC.name: -150,
    }
