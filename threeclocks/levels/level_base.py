"""Module base level."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.config.constants import N_LEVELS
from threeclocks.clean_new_game import clean_entity_ids
from threeclocks.config.settings import Settings
from threeclocks.models.experience_points import ExperiencePoints
from threeclocks.resources import Resource
from threeclocks.models.actors.actor_types import ActorType
from threeclocks.tools.logger.logger import log


class LevelException(Exception):
    pass


class Level:
    """Represents a base level.
    It is not intended to be instantiated.
    """

    def __init__(self, id_, game, name=None):
        self.id = id_
        self.name = name or str(self.id)
        self.game = game
        self.player = game.player
        self.completed = False
        self.all_sprites = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.clocks = pg.sprite.Group()
        self.mines = pg.sprite.Group()
        self.explosions = pg.sprite.Group()

        self._add_actors()

    def _add_actors(self):
        self._add_actors_hook()
        self._sprites_all_add()

    def _add_actors_hook(self):
        pass

    def _sprites_all_add(self):
        for sprite in self.clocks:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.mines:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.explosions:
            self.all_sprites.add(sprite)

    def update(self):
        self.all_sprites.update()

        if not self.completed and not self.clocks:
            self.completed = True
            self.player.stats['score'] += ExperiencePoints.xp_points['game_level']
            for clock in self.game.clock_sprites:
                clock.kill_hook()

    def draw(self):
        screen = self.game.screen
        screen.blit(Resource.images['background'], (0, 0))
        screen.blit(Resource.images['board'], (Settings.board_x, Settings.board_y))
        screen.blit(
            Resource.images['help_key'], (Settings.help_key_pos[0], Settings.help_key_pos[1]))
        screen.blit(Resource.images['logo_jp'], (20, 20))
        self.all_sprites.draw(screen)

    def add_actors(self, actors):
        for actor in actors:
            self.game.is_log_debug and log.debug(f"Add actor {actor.id} to level {self.id}")
            if actor.type == ActorType.CLOCK_TIMER_A:
                self.game.clock_sprites.add(actor)

    @staticmethod
    def factory(levels_module, game):
        return [getattr(levels_module, f"Level{level_id}")(level_id, game)
                for level_id in range(1, N_LEVELS + 1)]

    @staticmethod
    def levels_completed_ids(game):
        return [x.id for x in game.levels if x.completed]

    @staticmethod
    def levels_completed_names(game):
        return [x.name for x in game.levels if x.completed]

    @staticmethod
    def levels_completed_count(game):
        return sum(1 for x in game.levels if x.completed)

    @staticmethod
    def clean_entity_ids():
        clean_entity_ids()
