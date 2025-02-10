"""Module clean_new_game."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.models.actors.actors import Actor
from threeclocks.models.clocks import ClockBase
from threeclocks.models.special_effects.light import Light


def clean_entity_ids():
    Actor.actors.clear()
    Actor.type_id_count.clear()
    ClockBase.type_id_count.clear()
    Light.type_id_count.clear()
