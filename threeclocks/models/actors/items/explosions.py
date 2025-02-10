"""Module explosions."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.config.constants import BM_EXPLOSIONS_FOLDER
from threeclocks.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType,
    )
from threeclocks.models.actors.actors import ActorItem
from threeclocks.models.stats import Stats


class Explosion(ActorItem):
    """Represents an explosion.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_folder = BM_EXPLOSIONS_FOLDER
        self.file_name_key = 'explosions'
        self.images_sprite_no = 8
        self.base_type = ActorBaseType.EXPLOSION
        self.category_type = ActorCategoryType.EXPLOSION
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.health = self.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        self.animation_speed = 0.4
        self.transparency_alpha = True
        self.cannot_be_copied = True

        super().__init__(x, y, game, name=name)

    def update_after_inc_index_hook(self):
        if self.frame_index >= self.images_sprite_no:
            self.kill()
            self.game.player.is_alive = False

        # Check if we hit any mine
        mines_hit_list = pg.sprite.spritecollide(
            self, self.game.level.mines, False)
        for mine in mines_hit_list:
            mine.explosion()

    def update_when_hit(self):
        """Cannot be hit."""
        pass


class ExplosionA(Explosion):
    """Represents an explosion of type A."""

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None):
        self.file_mid_prefix = 't1'
        self.type = ActorType.EXPLOSION_A
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner)
        self.power = self.power_total = 350
