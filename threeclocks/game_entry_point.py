"""Module game_entry_point."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ['Game']

import pygame as pg

from threeclocks.models.actors.actors import Actor
from threeclocks.models.actors.player import Player

from threeclocks.config.constants import (
    FONT_DEFAULT_NAME, FONT_FIXED_DEFAULT_NAME,
    LOG_GAME_BEATEN, LOG_GAME_OVER,
    N_LEVELS,
    )
from threeclocks.help_info import DebugInfo, HelpInfo
from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.resources import Resource
from threeclocks.score_bars import ScoreBar
from threeclocks import screens
from threeclocks.config.settings import Settings, DEFAULT_MUSIC_VOLUME
from threeclocks.tools.utils.colors import Color
from threeclocks import levels
from threeclocks.levels import Level
from threeclocks.models.actors.actor_types import ActorType
from threeclocks.models.sprite_selectors import SelectorA
from threeclocks.persistence.persistence_settings import (
    PERSISTENCE_PATH_DEFAULT,
    PersistenceSettings,
    )
from threeclocks.persistence import persistence
from threeclocks.ui.ui_manager.ui_manager import UIManager
from threeclocks.models.experience_points import ExperiencePoints
from threeclocks.tools.logger.logger import log


class Game:
    """Represents a 'Three Clocks' game."""
    is_exit_game = False
    is_over = False
    is_first_game = True
    is_log_debug = False
    current_game = 0
    current_time = None
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None
    no_log_datetime = False
    stdout_log = False
    ui_manager = None
    new_game = False

    def __init__(self, is_debug=None, is_full_screen=False,
                 no_log_datetime=None, stdout_log=None,
                 is_no_display_scaled=None):
        self.name = "Three Clocks"
        self.name_short = "Three Clocks"
        self.start_time = None
        self.done = None
        self.player = None
        self.winner = None
        self.is_debug = is_debug
        self.is_paused = False
        self.is_start_screen = True
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_exit_curr_game_confirm = False
        self.is_music_paused = False
        self.sound_effects = True
        self.show_fps = False
        self.show_grid = False
        self.current_position = False
        self.persistence_path = PERSISTENCE_PATH_DEFAULT
        self.persistence_path_from_user = ''
        self.levels = []
        self.levels_qty = 0
        self.level = None
        self.level_no = 0
        self.level_no_old = None
        self.clock = False
        self.active_sprites = None
        self.clock_sprites = None
        self.selector_sprites = pg.sprite.Group()
        self.selector_sprite = None
        self.score_bars = None
        self.help_info = None
        self.debug_info = None
        self.current_song = 0
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.screen_help = None
        self.selected_sprite = None
        self.mouse_pos = (0, 0)
        self.is_continue_game = False
        self.is_load_user_game = False
        self.can_user_leave_game = True

        Game.is_exit_game = False
        if Game.current_game > 0:
            Game.is_first_game = False

        if Game.is_first_game:
            self._first_game_setup(
                no_log_datetime, stdout_log, is_full_screen,
                is_no_display_scaled)
        else:
            self.player = Player.players[0]
            self.player.reset_stats()

        self.current_time_delta = pg.time.get_ticks() / 1000.0

        # Initialize screens
        self.screen_exit_current_game = screens.ScreenExitCurrentGame(self)
        self.screen_help = screens.ScreenHelp(self)
        self.screen_pause = screens.ScreenPause(self)
        self.screen_game_over = screens.ScreenGameOver(self)

    def _first_game_setup(self, no_log_datetime, stdout_log,
                          is_full_screen, is_no_display_scaled=None):
        Game.no_log_datetime = no_log_datetime
        Game.stdout_log = stdout_log

        # Calculate settings
        pg_display_info = pg.display.Info()
        Settings.display_start_width = pg_display_info.current_w
        Settings.display_start_height = pg_display_info.current_h
        Settings.calculate_settings(full_screen=is_full_screen)

        # Set screen to the settings configuration
        Game.size = Settings.screen_width, Settings.screen_height
        Game.full_screen_flags = pg.FULLSCREEN if is_no_display_scaled else pg.FULLSCREEN | pg.SCALED
        Game.normal_screen_flags = pg.SHOWN if is_no_display_scaled else pg.SHOWN | pg.SCALED
        Game.screen_flags = Game.full_screen_flags if Settings.is_full_screen else Game.normal_screen_flags
        Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)

        # Load and render resources
        Resource.load_and_render_background_images()
        Resource.load_and_render_scorebar_images_and_txt()
        Resource.load_sound_resources()
        Resource.load_music_song(self.current_song)

        # Render characters in some colors to use it as a cache
        libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
        libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)

        # Initialize music
        pg.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)
        pg.mixer.music.play(loops=-1)
        if self.is_music_paused:
            pg.mixer.music.pause()

        # Initialize persistence settings if necessary
        PersistenceSettings.init_settings(self.persistence_path)

        # Initialize UI
        Game.ui_manager = UIManager(self)

        self.player = Player("Player 1", game=self)

    @staticmethod
    def set_is_exit_game(is_exit_game):
        Game.is_exit_game = is_exit_game

    def clean_game_data(self):
        self.__class__.ui_manager.clean_game_data()
        Level.clean_entity_ids()
        Actor.type_id_count.clear()
        self.__class__.ui_manager.clean_game_data()

    def run_explosion_mines_in_current_level(self):
        for mine in self.level.mines:
            mine.explosion()
        self.sound_effects and Resource.mine_click_sound.play()

        for clock in self.clock_sprites:
            clock.die_hard()

    def handle_sprite_selector(self):
        # Handle when the player clicks on a mine
        sprite = self.selector_sprite.get_pointed_sprite(group=self.level.mines)
        if sprite and sprite.type.name == ActorType.MINE_LILAC.name:
            self.selected_sprite = sprite
            self.is_log_debug and log.debug(f"Selected sprite: {self.selected_sprite.id}")
            self.sound_effects and Resource.mine_click_sound.play()
            self.selected_sprite.explosion()
            return

        # Handle when the player clicks on a clock
        sprite = self.selector_sprite.get_pointed_sprite(group=self.level.clocks)
        if sprite and sprite.type.name == ActorType.CLOCK_A.name:
            self.selected_sprite = sprite
            self.is_log_debug and log.debug(f"Selected sprite: {self.selected_sprite.id}")
            self.player.stats['score'] += \
                ExperiencePoints.xp_points[self.selected_sprite.type.name]
            self.sound_effects and Resource.clock_click_sound.play()
            self.selected_sprite.set_on_to_explode(owner=self.selected_sprite)
            return

        self.selected_sprite = None

    def put_initial_actors_on_the_board(self):
        self.active_sprites = pg.sprite.Group()
        self.clock_sprites = pg.sprite.Group()
        self.selector_sprites = pg.sprite.Group()

        # Initialize levels
        self.levels = Level.factory(levels_module=levels, game=self)
        self.levels_qty = len(self.levels)
        self.level_no = 0
        self.level = self.player.level = self.levels[self.level_no]

        self.is_log_debug and log.debug("Waiting input from player")
        self.selector_sprite = SelectorA(0, 0, self)
        self.selector_sprites.add(self.selector_sprite)

        # Initialize persistence settings
        PersistenceSettings.init_settings(
            self.persistence_path_from_user or self.persistence_path)
        if self.is_continue_game:
            persistence.load_game_data(self)
        if self.is_load_user_game:
            PersistenceSettings.init_settings(self.persistence_path)

    def update_screen(self):
        # Handle game screens
        if self.is_paused or self.is_full_screen_switch:
            self.screen_pause.start_up(
                is_full_screen_switch=self.is_full_screen_switch)
        if self.is_help_screen:
            self.screen_help.start_up()
        elif self.is_exit_curr_game_confirm:
            self.screen_exit_current_game.start_up()
            if self.done:
                self.player.is_alive and persistence.persist_game_data(self)
                self.clean_game_data()
        elif Game.is_over:
            self.screen_game_over.start_up()
            if self.done:
                persistence.clear_all_persisted_data()
                self.clean_game_data()
        else:
            # Draw sprites, etc.
            self.level.draw()

            if self.show_grid:
                libg_jp.draw_grid(
                    Game.screen, Settings.cell_size, Settings.screen_width,
                    Settings.screen_height, Settings.screen_near_top, Color.DARK_BLUE)

            # Update score bars
            self.score_bars.update(self.level_no, self.level_no_old)
            if self.level_no != self.level_no_old:
                self.level_no_old = self.level_no

            self.active_sprites.draw(Game.screen)

            for clock in self.clock_sprites:
                clock.draw_text()

            # Update and draw selectors
            self.selector_sprite.update()
            self.selector_sprites.draw(Game.screen)

    def update_status_if_game_over(self):
        self.is_over = True
        self.done = True

    def _game_loop(self):
        self.update_state_counter = -1
        while not self.done:
            self.current_time = pg.time.get_ticks()
            self.current_time_delta = pg.time.get_ticks() / 1000.0

            # Increase and check counter to delay stats x iterations
            self.update_state_counter += 1
            if self.update_state_counter > 16:
                self.update_state_counter = 0

            for event in pg.event.get():
                if event.type == pg.QUIT \
                        or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if self.can_user_leave_game:
                        self.is_exit_curr_game_confirm = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        if self.can_user_leave_game:
                            self.is_paused = True
                    elif event.key == pg.K_d :
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info()
                    elif event.key == pg.K_m and pg.key.get_mods() & pg.KMOD_LALT:
                        self.is_music_paused = not self.is_music_paused
                        if self.is_music_paused:
                            pg.mixer.music.pause()
                        else:
                            pg.mixer.music.unpause()
                    elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_LALT:
                        self.sound_effects = not self.sound_effects
                    elif event.key == pg.K_F1:
                        if not self.is_exit_curr_game_confirm and self.can_user_leave_game:
                            self.is_help_screen = not self.is_help_screen
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                        if pg.key.get_mods() & pg.KMOD_LALT \
                                and self.can_user_leave_game:
                            self.is_full_screen_switch = True
                elif event.type == pg.MOUSEBUTTONDOWN \
                     and pg.mouse.get_pressed(num_buttons=3)[0]:
                    self.mouse_pos = pg.mouse.get_pos()
                    self.handle_sprite_selector()

                self.mouse_pos = pg.mouse.get_pos()

            # Update sprites
            self.active_sprites.update()
            self.level.update()
            self.clock_sprites.update()

            # Start the next level if necessary
            if self.level.completed and self.level_no < N_LEVELS - 1:
                self.level_no += 1
                self.level = self.levels[self.level_no]

            # Check if the player has beaten or lost the game,
            # but skip the first 4 iterations
            if self.update_state_counter == 4:
                if Level.levels_completed_count(self) >= self.levels_qty:
                    self.winner = self.player
                    log.info(LOG_GAME_BEATEN)
                elif not self.player.is_alive:
                    Game.is_over = True
                    log.info(LOG_GAME_OVER)
                if self.winner:
                    self.player.stats['score'] += \
                        ExperiencePoints.xp_points['beat_the_game']
                    # Force updating the game screen to update the score
                    self.update_state_counter = 0
                    self.update_screen()
                if self.winner or Game.is_over:
                    Game.is_over = True

            self.update_screen()

            if self.is_paused:
                self.clock.tick(Settings.fps_paused)
            else:
                self.clock.tick(Settings.fps)
            pg.display.flip()

    def start(self):
        pg.mouse.set_visible(False)
        Game.is_exit_game = False
        Game.is_over = False

        Game.current_game += 1
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()

        self.put_initial_actors_on_the_board()

        # Initialize score bars
        self.score_bars = ScoreBar(self)

        # Render text frequently used only if it is the first game
        if Game.is_first_game:
            Resource.render_text_frequently_used(self)

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self)

        not self.done and log.info("Start game")
        self._game_loop()
