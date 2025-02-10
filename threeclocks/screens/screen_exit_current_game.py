"""Module screen_exit_current_game."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.resources import Resource
from threeclocks.config.settings import Settings
from threeclocks.screens.screen_base import ScreenBase


class ScreenExitCurrentGame(ScreenBase):
    """Represents an Exit Current Game screen."""

    def __init__(self, game):
        super().__init__(game)

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['exit_current_game_confirm'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_center'])

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if (event.type == pg.QUIT
                    or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
                self.game.done = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if (event.key in (pg.K_KP_ENTER, pg.K_RETURN)
                        and pg.key.get_mods() & pg.KMOD_LCTRL):
                    self.done = True

    def _game_loop(self):
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)
            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)

        self._game_loop()

        self.game.is_exit_curr_game_confirm = False
