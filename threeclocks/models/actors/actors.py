"""Module actors."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
from os import path

import pygame as pg

from threeclocks.tools.logger.logger import log
from threeclocks.config.constants import FILE_NAMES
from threeclocks.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType,
    )
from threeclocks.tools.utils.colors import Color


class Actor(pg.sprite.Sprite):
    """Represents an actor.
    It is not intended to be instantiated.
    """
    type_id_count = Counter()
    # key: sprite_sheet_data_id, value: (image, frames)
    sprite_images = {}
    actors = {}

    def __init__(self, x, y, game, name=None):
        super().__init__()
        Actor.type_id_count[self.type] += 1
        self.id = f"{self.type.name}_{Actor.type_id_count[self.type]:05d}"
        self.game = game
        self.last_shot_time = 0
        self.time_between_shots_base = 1200
        self.target_of_spells_count = Counter()
        self.direction = 1

        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.NONE

        if not getattr(self, 'category_type', None):
            self.category_type = ActorCategoryType.NONE

        if self.category_type.name == ActorCategoryType.CLOCK.name:
            Actor.actors[self.id] = self

        if not getattr(self, 'type', None):
            self.type = ActorType.NONE

        if not getattr(self, 'file_folder', None):
            self.file_folder = None
        if not getattr(self, 'file_mid_prefix', None):
            self.file_mid_prefix = None
        if not getattr(self, 'file_prefix', None):
            self.file_prefix = None
        if not getattr(self, 'file_name_key', None):
            self.file_name_key = None

        if not getattr(self, 'images_sprite_no', None):
            self.images_sprite_no = 1
        if not getattr(self, 'animation_speed', None):
            self.animation_speed = 0.1
        if not getattr(self, 'frame_index', None):
            self.frame_index = 0

        if not getattr(self, 'is_item', None):
            self.is_item = False

        if not getattr(self, 'transparency_alpha', None):
            self.transparency_alpha = False

        self.name = name or 'unnamed'

        self.init_before_load_sprites_hook()
        self._load_sprites()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.init_after_load_sprites_hook()
        self.game.is_log_debug and log.debug(f"Create actor of type: {self.type}")

    def _load_sprites(self):
        if not Actor.sprite_images.get(self.type.name):
            frames = []
            image = None
            for i in range(self.images_sprite_no):
                if self.transparency_alpha:
                    image = pg.image.load(
                        self.file_name_im_get(
                        self.file_folder, self.file_name_key,
                        self.file_mid_prefix, suffix_index=i+1
                        )).convert_alpha()
                else:
                    image = pg.image.load(self.file_name_im_get(
                        self.file_folder, self.file_name_key,
                        self.file_mid_prefix, suffix_index=i+1
                    )).convert()
                    image.set_colorkey(Color.BLACK)
                frames.append(image)
            Actor.sprite_images[self.type.name] = (image, frames)
            self.image = frames[0]
        else:
            self.image = Actor.sprite_images[self.type.name][0]

    def init_before_load_sprites_hook(self):
        pass

    def init_after_load_sprites_hook(self):
        pass

    def update(self):
        self.frame_index += self.animation_speed
        self.update_after_inc_index_hook()
        if self.frame_index >= self.images_sprite_no:
            self.frame_index = 0

        self.update_sprite_image()
        self.update_when_hit()

    def update_sprite_image(self):
        self.image = Actor.sprite_images[self.type.name] \
            [self.direction][int(self.frame_index)]

    def update_after_inc_index_hook(self):
        pass

    def update_when_hit(self):
        pass

    def kill_hook(self):
        self.kill()

    def explosion(self):
        pass

    @staticmethod
    def factory(actors_module, type_name, x, y, game, kwargs):
        return getattr(actors_module, type_name)(x, y, game, **kwargs)

    @staticmethod
    def get_actor(actor_id):
        return Actor.actors[actor_id]

    @staticmethod
    def file_name_im_get(folder, file_name_key, mid_prefix, suffix_index):
        return path.join(
            folder, f"{FILE_NAMES[file_name_key][0]}"
            f"{'_' if mid_prefix else ''}"
            f"{mid_prefix or ''}"
            f"_{suffix_index:02d}.{FILE_NAMES[file_name_key][1]}")


class ActorItem(Actor):
    """Represents an item actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.base_type = ActorBaseType.ITEM
        super().__init__(x, y, game, name=name)

    @staticmethod
    def get_items_stats_to_persist(game):
        """Returns a dictionary with all the items' stats to persist."""
        res = {'game_levels': {}}
        levels = res['game_levels']
        levels[game.level.id] = {
            'items': {},
            }
        for item in game.level.items:
            levels[game.level.id]['items'][item.id] = {
                'category_type': item.category_type.name,
                'type': item.type.name,
                }
        return res

    @staticmethod
    def get_items_not_initial_actor_stats_to_persist(game):
        """Returns a dictionary with the items' stats to persist
        only for items not initially in a fresh game.
        """
        res = {'game_levels': {}}
        levels = res['game_levels']
        levels[game.level.id] = {
            'items': {},
            }
        for item in game.clock_sprites:
            levels[game.level.id]['items'][item.id] = {
                'base_type': item.base_type.name,
                'category_type': item.category_type.name,
                'type': item.type.name,
                'type_name': item.__class__.__name__,
                'dx': item.owner.text_dx,
                'dy': item.owner.text_dy,
                'owner': item.owner.id,
                'remaining_time_in_secs': item.clock.get_time(),
                }
        return res
