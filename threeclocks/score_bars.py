"""Module score_bars."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.config.constants import SCORE_BAR_HEIGHT
from threeclocks.tools.utils.colors import Color
from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.resources import Resource
from threeclocks.config.settings import Settings


class ScoreBar:
    """Represents a score bar."""

    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.level_no = None
        self.level_no_old = None
        self.screen = pg.Surface((Settings.screen_width, SCORE_BAR_HEIGHT))

    def draw_chars_render_text(self, text, x, y, color=Color.YELLOW):
        libg_jp.draw_text_rendered(text, x, y, self.screen, color)

    def render_stats_if_necessary(self, x, y, stats_name):
        # player stats
        libg_jp.draw_text_rendered(text=f'{self.player.stats[stats_name]}',
                                        x=x, y=y, screen=self.screen, color=Color.GREEN)
        if self.player.stats[stats_name] != self.player.stats_old[stats_name]:
            self.player.stats_old[stats_name] = self.player.stats[stats_name]

    def draw_stats(self):
        # Draw player score titles
        self.screen.blit(*Resource.txt_surfaces['sb_score_title1'])
        self.screen.blit(*Resource.txt_surfaces['sb_level'])

        # Draw score stats and render them if needed
        self.render_stats_if_necessary(
            Settings.score_pos_score1[1],
            Settings.screen_bar_near_top, 'score')

        libg_jp.draw_text_rendered(
            text=f'{self.level_no + 1} of {self.game.levels_qty}',
            x=Settings.score_pos_level[1],
            y=Settings.screen_bar_near_top,
            screen=self.screen, color=Color.GREEN)

    def update(self, level_no, level_no_old):
        if self.game.update_state_counter != 0:
            self.game.screen.blit(self.screen)
            return

        self.level_no = level_no
        self.level_no_old = level_no_old

        self.screen = pg.Surface((Settings.screen_width, SCORE_BAR_HEIGHT))

        self.draw_stats()
        self.screen.set_colorkey(Color.BLACK)
        self.game.screen.blit(self.screen)
