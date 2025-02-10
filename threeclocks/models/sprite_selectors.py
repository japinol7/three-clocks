"""Module selectors."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from threeclocks.config.constants import BM_SELECTORS_FOLDER
from threeclocks.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType,
    )
from threeclocks.models.actors.actors import ActorItem
from threeclocks.tools.utils.colors import Color
from threeclocks.models.special_effects.light import Light, LightGrid
from threeclocks.config.settings import Settings


class Selector(ActorItem):
    """Represents a selector.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_SELECTORS_FOLDER
        self.file_name_key = 'im_selectors'
        self.images_sprite_no = 1
        self.base_type = ActorBaseType.SELECTOR
        self.category_type = ActorCategoryType.SELECTOR
        self.light_grid = None
        self.light_grid_surf_size = 34, 34
        self.light_grid_surf_size_half = \
            self.light_grid_surf_size[0] // 2, self.light_grid_surf_size[1] // 2
        self.light_color = Color.GREEN
        self.sel_selected_actor_id = None
        self.sel_selected_actor_pos = 0, 0
        self.sel_selected_actor_world_shift = 0
        self.sel_selected_actor_world_shift_top = 0

        super().__init__(x, y, game, name=name)

        self._create_light()

    def update_sprite_image(self):
        pass

    def _create_light(self):
        self.light_grid = LightGrid(self.light_grid_surf_size)
        self.light_grid.add_light(
            Light((0, 0), radius=18, color=self.light_color, alpha=255),
            )

    def update_after_inc_index_hook(self):
        mx, my = self.game.mouse_pos
        self.rect.centerx, self.rect.centery = mx, my

        if Settings.has_selector_no_light:
            return

        # Create a surface with only the part of the screen
        # that is needed for the light grid render
        sub_screen_rect = pg.Rect(
            mx - self.light_grid_surf_size_half[0],
            my - self.light_grid_surf_size_half[1],
            self.light_grid_surf_size[0],
            self.light_grid_surf_size[1])
        grid_surface = pg.Surface(sub_screen_rect.size)
        grid_surface.blit(self.game.screen, (0, 0), sub_screen_rect)

        # Render all the lights of the light grid
        for light in self.light_grid.lights.values():
            light.set_color(self.light_color, override_alpha=True)
            light.position = (self.light_grid_surf_size_half[0],
                              self.light_grid_surf_size_half[1])
        self.light_grid.render(grid_surface)
        self.game.screen.blit(grid_surface, sub_screen_rect)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def get_pointed_select_sprite(self, group=None):
        if group is None:
            group = self.game.level.items

        sprite_hit_list = pg.sprite.spritecollide(
            self, group, False)
        if sprite_hit_list:
            for sprite_hit in sprite_hit_list:
                return sprite_hit

        return None

    def get_pointed_sprite(self, group=None):
        sprite = self.get_pointed_select_sprite(group=group)
        return sprite


class SelectorA(Selector):
    """Represents a selector of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.SELECTOR_A
        super().__init__(x, y, game, name=name)
