"""Module level 2."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.models.actors.items import ClockA, MineLilac
from threeclocks.levels.level_base import Level


class Level2(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add clocks
        self.clocks.add([
            ClockA(567, 260, self.game, time_in_secs=4, text_dy=-90),
            ClockA(950, 260, self.game, time_in_secs=2, text_dy=-90),
            ClockA(1332, 260, self.game, time_in_secs=5, text_dy=-90),
            ])

        # Add mines arranged in circles around each clock
        for clock in self.clocks:
            self._add_circle_of_mines(clock, angle=0, radius=28)
            self._add_circle_of_mines(clock, angle=0, radius=68)
            self._add_circle_of_mines(clock, angle=0, radius=100, angle_increment=18)

    def _add_circle_of_mines(self, clock, angle, radius, angle_increment=20):
        center_point_x, center_point_y = clock.rect.x + 5, clock.rect.y + 5
        while angle <= 360:
            vector = pg.math.Vector2(0, -radius).rotate(angle)
            point_x, point_y = center_point_x + vector.x, center_point_y + vector.y
            self.mines.add([
                MineLilac(point_x, point_y, self.game),
                ])
            angle += angle_increment
