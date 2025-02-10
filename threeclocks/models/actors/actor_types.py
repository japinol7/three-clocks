"""Module actor_types."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum


class ActorBaseType(Enum):
    NONE = 0
    ITEM = 1
    EXPLOSION = 11
    SELECTOR = 21


class ActorCategoryType(Enum):
    NONE = 0
    CLOCK = 1
    MINE = 2
    EXPLOSION = 31
    SELECTOR = 41


class ActorType(Enum):
    NONE = 0
    # Clocks
    CLOCK_A = 1
    # Mines
    MINE_LILAC = 2
    # Explosions
    EXPLOSION_A = 41
    # Clock Counters
    CLOCK_TIMER_A = 51
    CLOCK_STOPWATCH_A = 52
    # Selectors
    SELECTOR_A = 71
