"""Module player."""
__author__ = 'Joan A. Pinol  (japinol)'

from abc import ABC, abstractmethod

from threeclocks.tools.logger.logger import log


class PlayerBase(ABC):
    players = []

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.is_alive = True
        self.stats = {}
        self.stats_old = {}

        self.reset_stats()

        self.__class__.players.append(self)
        self.game.is_log_debug and log.debug(f"Create {self}")

    @abstractmethod
    def update(self, board):
        pass

    def __str__(self):
        return f"Player: {self.name}. Class: {self.__class__.__name__}"

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"({self.name})"

    def reset_stats(self):
        self.is_alive = True
        self.stats = {
            'score': 0,
            }
        self.stats_old = {key: None for key in self.stats}

    def die_hard(self):
        self.is_alive = False


class Player(PlayerBase):

    def __init__(self, name, game):
        super().__init__(name, game)

    def update(self, board):
        super().update(board)

    @staticmethod
    def get_stats_to_persist(game):
        """Returns a dictionary with all the player's stats to persist."""
        res = {'player': {}}
        pc = game.player
        res['player'] = {
            'score': pc.stats['score'],
            'current_level': game.level.id,
            'sound_effects': game.sound_effects,
            'is_music_paused': game.is_music_paused,
            }
        return res
