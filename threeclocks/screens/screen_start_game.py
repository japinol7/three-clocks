"""Module screen_start_game."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg
import pygame_gui as pgui

from threeclocks.tools.utils.colors import Color
from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.resources import Resource
from threeclocks.config.settings import Settings
from threeclocks.screens.screen_base import ScreenBase
from threeclocks.tools.logger.logger import log


class ScreenStartGame(ScreenBase):
    """Represents a Start Game screen."""

    def __init__(self, game):
        super().__init__(game)

        libg_jp.render_text(
            '– Press Ctrl + Alt + Enter to Start –', Settings.board_base_center[0],
                Settings.board_base_center[1] - 190,
                Resource.txt_surfaces, 'game_start', color=Color.BLUE,
                size=40, align="center")
        libg_jp.render_text(
            '– Press Ctrl + Alt + Enter to Start –', Settings.board_base_center[0] / 1.002,
                Settings.board_base_center[1] / 1.004 - 190,
                Resource.txt_surfaces, 'game_start_2', color=Color.CYAN,
                size=40, align="center")

    def _draw(self):
        super()._draw()

        self.game.screen.blit(Resource.images['screen_start'],
            (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(
            Resource.images['help_key'], (Settings.help_key_pos[0], Settings.help_key_pos[1]))
        self.game.screen.blit(Resource.images['logo_jp'], (20, 20))
        self.game.screen.blit(Resource.images['board'], (Settings.board_x, Settings.board_y))

        self.game.screen.blit(*Resource.txt_surfaces['game_start'])
        self.game.screen.blit(*Resource.txt_surfaces['game_start_2'])

    def _events_handle(self, events):
        super()._events_handle(events)
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.game.set_is_exit_game(True)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.game.screen_help.start_up()
                    self.done = True
                elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                    if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                        self.game.__class__.new_game = True
                elif event.key == pg.K_SPACE:
                    if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                        self.game.is_continue_game = True
                elif event.key == pg.K_KP_DIVIDE:
                    if self.game.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL \
                            and pg.key.get_mods() & pg.KMOD_LALT:
                        if log.level != logging.DEBUG:
                            log.setLevel(logging.DEBUG)
                            self.game.__class__.is_log_debug = True
                            log.info("Set logger level to: Debug")
                        else:
                            log.setLevel(logging.INFO)
                            self.game.__class__.is_log_debug = False
                            log.info("Set logger level to: Info")
            # Manage In Game UI events
            self.game.ui_manager.ui_main_menu.manager.process_events(event)
            if event.type == pgui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == self.game.ui_manager.ui_main_menu.items[
                    'delete_saved_game_confirm_dialog']:
                    self.game.ui_manager.ui_main_menu.delete_game_directory_action()

        if self.game.is_exit_game:
            self.game.is_start_screen = False
            self.done = True
        elif self.game.__class__.new_game:
            self.game.is_start_screen = False
            self.game.is_continue_game = False
            self.done = True
        elif self.game.is_continue_game:
            self.game.is_start_screen = False
            self.done = True

        if self.done:
            self.game.ui_manager.ui_main_menu.hide_additional_game_items()
            self.game.ui_manager.ui_main_menu.clean_ui_items()

    def _game_loop(self):
        ui_ingame_manager = self.game.ui_manager.ui_main_menu.manager
        clock = pg.time.Clock()
        while not self.done:
            events = pg.event.get()
            self._events_handle(events)

            try:
                ui_ingame_manager.update(self.game.current_time_delta)
            except Exception as e:
                log.warning(f"ERROR in pygame-gui libray: {e}")

            self._draw()
            ui_ingame_manager.draw_ui(self.game.screen)

            pg.display.flip()
            clock.tick(Settings.fps_paused)

    def start_up(self, current_time=None, *args, **kwargs):
        super().start_up(current_time=self.game.current_time)

        self.game.is_start_screen = True
        self.game.persistence_path_from_user = ''

        self._game_loop()
