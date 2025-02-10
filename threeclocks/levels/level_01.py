"""Module level 1."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.models.actors.items import ClockA, MineLilac
from threeclocks.levels.level_base import Level


class Level1(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add clocks
        self.clocks.add([
            ClockA(567, 260, self.game, time_in_secs=3),
            ClockA(950, 260, self.game, time_in_secs=5),
            ClockA(1332, 260, self.game, time_in_secs=5),
            ])

        # Add mines
        self.mines.add([
            MineLilac(762, 580, self.game),
            MineLilac(1147, 580, self.game),
            ])
