"""Module mines."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.config.constants import BM_MINES_FOLDER
from threeclocks.models.actors.actor_types import ActorCategoryType, ActorType
from threeclocks.models.actors.actors import ActorItem
from threeclocks.models.stats import Stats
from threeclocks.models.actors.items.explosions import ExplosionA


class Mine(ActorItem):
    """Represents a mine.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_MINES_FOLDER
        self.file_name_key = 'im_mines'
        self.images_sprite_no = 7
        self.category_type = ActorCategoryType.MINE
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        super().__init__(x, y, game, name=name)

    def explosion(self, owner=None):
        """When hit, explodes."""
        super().explosion()

        explosion = self.explosion_class(
            self.rect.x - self.rect.w // 2, self.rect.y - 60,
            self.game, owner=owner)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)
        self.kill_hook()

        self.game.can_user_leave_game = False


class MineLilac(Mine):
    """Represents a lilac mine."""

    def __init__(self, x, y, game, name=None):
        self.explosion_class = ExplosionA
        self.file_mid_prefix = 't2'
        self.type = ActorType.MINE_LILAC
        super().__init__(x, y, game, name=name)
