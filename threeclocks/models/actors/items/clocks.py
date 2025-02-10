"""Module clocks."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.config.constants import BM_CLOCKS_FOLDER
from threeclocks.models.actors.actor_types import (
    ActorCategoryType,
    ActorType,
    )
from threeclocks.models.actors.actors import ActorItem
from threeclocks.models.stats import Stats
from threeclocks.models.clocks import ClockTimer
from threeclocks.tools.utils.colors import Color
from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.tools.logger.logger import log


class Clock(ActorItem):
    """Represents a clock.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, owner=None,
                 text_dx=0, text_dy=44):
        self.file_folder = BM_CLOCKS_FOLDER
        self.file_name_key = 'im_clocks'
        self.owner = owner or game.player
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.CLOCK
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.cannot_be_copied = True
        self.text_dx = text_dx
        self.text_dy = text_dy

        super().__init__(x, y, game, name=name)

        self.text_img_w = 80

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def set_on(self):
        pass


class ClockA(Clock):
    """Represents a clock of type A. It generates a clock timer A"""

    def __init__(self, x, y, game, time_in_secs, name=None,
                 text_dx=0, text_dy=44):
        self.file_mid_prefix = '01'
        self.type = ActorType.CLOCK_A
        self.time_in_secs = time_in_secs
        super().__init__(
            x, y, game, name=name, text_dx=text_dx, text_dy=text_dy)

    def set_on(self, owner=None):
        clock = ClockTimerA(
            self.text_dx, self.text_dy, self.game, self.time_in_secs, owner=owner)
        self.game.clock_sprites.add([clock])
        self.kill()

    def set_on_to_explode(self, owner=None):
        clock = ClockTimerA(
            self.text_dx, self.text_dy, self.game, self.time_in_secs, owner=owner)
        clock.clock.trigger_method = self.game.run_explosion_mines_in_current_level

        self.game.clock_sprites.add([clock])
        self.kill()


class ClockTimerA(Clock):
    """Represents a clock timer of type A."""

    def __init__(self, dx, dy, game, time_in_secs, name=None,
                 owner=None, x_centered=True, y_on_top=True):
        self.file_mid_prefix = 'timer_01'
        self.type = ActorType.CLOCK_TIMER_A

        super().__init__(-500, 0, game, name=name, owner=owner)

        self.clock = ClockTimer(
            self.game, time_in_secs, trigger_method=self.die_hard)

        self.dx, self.dy = 0, 0
        if x_centered:
            self.dx = (self.owner.rect.w - self.text_img_w) // 2
        self.dx += dx
        if y_on_top:
            self.dy = -7
        self.dy += dy

    def update(self):
        self.rect.bottom = self.owner.rect.y + self.dy
        self.rect.x = self.owner.rect.x + self.dx

        super().update()
        self.clock.tick()

    def draw_text(self):
        libg_jp.draw_text_rendered(
            text=self.clock.get_time_formatted(),
            x=self.rect.x + 12, y=self.rect.y + 3,
            screen=self.game.screen, color=Color.GREEN)

    def die_hard(self):
        self.game.is_log_debug and log.debug(
            f"{self.id} killed when {self.clock.id} "
            f"ticked {self.clock.get_time()} secs.")
        self.kill()
