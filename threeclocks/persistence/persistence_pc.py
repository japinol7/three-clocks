"""Module persistence_pc."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy

from threeclocks.models.actors.player import Player
from threeclocks.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PersistenceSettings,
    )
from threeclocks.persistence.exceptions import (
    LoadGamePcException,
    )
from threeclocks.persistence.persistence_utils import (
    load_data_from_file,
    save_data_to_file,
    )
from threeclocks.persistence.validations import (
    validate_load_data_game_basic_metadata,
    )
from threeclocks.tools.logger.logger import log


def persist_game_pc_data(game):
    game.is_debug and log.debug("Save current game PC")

    game_data = deepcopy(GAME_DATA_HEADER)
    pc_data = Player.get_stats_to_persist(game)
    game_data.update(pc_data)
    save_data_to_file(PersistenceSettings.settings['pc_file'], game_data)


def load_game_pc_data(game):
    game.is_debug and log.debug("Load last saved game PC")
    _load_pc_data(game)


def validate_load_data_basic_structure(pc_data):
    if (not pc_data or not isinstance(pc_data.get('saved_game_data'), dict)
            or not isinstance(pc_data.get('player'), dict)):
        raise LoadGamePcException("No game data or invalid format!")


def _load_pc_data(game):
    pc_data = load_data_from_file(PersistenceSettings.settings['pc_file'])

    validate_load_data_basic_structure(pc_data)
    validate_load_data_game_basic_metadata(pc_data)

    pc = game.player
    pc_data = pc_data['player']

    pc.stats.update({
        'score': pc_data['score'],
        })

    game.sound_effects = pc_data['sound_effects']
    game.is_music_paused = pc_data['is_music_paused']

    current_level = pc_data['current_level'] -1
    for level in game.levels[:current_level]:
        level.completed = True
