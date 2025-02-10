"""Module screen_pause."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg

from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.resources import Resource
from threeclocks.config.settings import Settings
from threeclocks.screens.screen_base import ScreenBase
from threeclocks.tools.logger.logger import log


class ScreenPause(ScreenBase):
    """Represents a pause screen."""

    def __init__(self, game):
        super().__init__(game)
        self.is_full_screen_switch = False

    def _full_screen_switch_hook(self):
        self.is_full_screen_switch = True

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.is_exit_curr_game_confirm = True
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.done = True
                elif event.key == pg.K_F1:
                    self.game.is_help_screen = True
                    self.done = True

            # Debug input events
            if self.game.is_debug and event.type == pg.KEYDOWN:
                if event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_LCTRL:
                    self.game.debug_info.print_debug_info()
                elif (event.key == pg.K_KP_DIVIDE and pg.key.get_mods() & pg.KMOD_LCTRL
                      and pg.key.get_mods() & pg.KMOD_LALT):
                    if log.level != logging.DEBUG:
                        log.setLevel(logging.DEBUG)
                        self.game.__class__.is_log_debug = True
                        log.info("Set logger level to: Debug")
                    else:
                        log.setLevel(logging.INFO)
                        self.game.__class__.is_log_debug = False
                        log.info("Set logger level to: Info")
                elif event.key == pg.K_g:
                    if pg.key.get_mods() & pg.KMOD_LCTRL \
                            and pg.key.get_mods() & pg.KMOD_RALT:
                        self.game.show_grid = not self.game.show_grid

            # Manage In Game UI events
            self.game.ui_manager.ui_ingame.manager.process_events(event)

            if self.done:
                self.game.ui_manager.ui_ingame.hide_additional_game_items()
                self.game.ui_manager.ui_ingame.clean_ui_items()

    def _game_loop(self):
        ui_ingame_manager = self.game.ui_manager.ui_ingame.manager
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                ui_ingame_manager.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self.game.screen.blit(self.background_screenshot, (0, 0))
            self.game.screen.blit(*Resource.txt_surfaces['game_paused'])

            ui_ingame_manager.draw_ui(self.game.screen)

            pg.display.flip()
            self.game.clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, is_full_screen_switch=False, *args, **kwargs):
        self.background_screenshot.blit(self.game.screen, (0, 0))

        pg.mouse.set_visible(True)
        self.is_full_screen_switch = is_full_screen_switch
        if self.is_full_screen_switch:
            self._full_screen_switch_hook()
            libg_jp.full_screen_switch(self.game)

        super().start_up(current_time=self.game.current_time)

        self._game_loop()

        self.game.is_paused = False
        self.game.is_full_screen_switch = False
        pg.mouse.set_visible(False)
