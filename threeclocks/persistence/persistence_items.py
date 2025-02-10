"""Module persistence_items."""
__author__ = 'Joan A. Pinol  (japinol)'

from copy import deepcopy

from threeclocks.models.actors.actor_types import ActorType
from threeclocks.models.actors.actors import Actor, ActorItem
from threeclocks.models.actors import items as items_module
from threeclocks.persistence.persistence_settings import (
    GAME_DATA_HEADER,
    PERSISTENCE_NO_SAVED_GAME_DATA_MSG,
    PersistenceSettings,
    )
from threeclocks.persistence.exceptions import (
    LoadGameItemsException,
    LoadGameNoSavedGameDataException,
    )
from threeclocks.persistence.persistence_utils import (
    load_data_from_file,
    save_data_to_file,
    )
from threeclocks.persistence.validations import (
    validate_load_data_game_basic_metadata,
    )
from threeclocks.tools.logger.logger import log


def persist_game_items_data(game):
    _persist_items_data(game)
    _persist_items_not_initial_data(game)


def load_game_items_data(game):
    _load_items_data(game)
    _load_items_not_initial_data(game)


def _persist_items_not_initial_data(game):
    game.is_debug and log.debug("Save current game items: Not initial actors")
    game_data = deepcopy(GAME_DATA_HEADER)
    items_data = ActorItem.get_items_not_initial_actor_stats_to_persist(game)
    game_data.update(items_data)
    save_data_to_file(PersistenceSettings.settings['items_new_file'], game_data)


def _persist_items_data(game):
    game.is_debug and log.debug("Save current game items")
    game_data = deepcopy(GAME_DATA_HEADER)
    items_data = ActorItem.get_items_stats_to_persist(game)
    game_data.update(items_data)
    save_data_to_file(PersistenceSettings.settings['items_file'], game_data)


def validate_load_data_basic_structure(items_data):
    if (not items_data or not isinstance(items_data.get('saved_game_data'), dict)
            or not isinstance(items_data.get('game_levels'), dict)):
        raise LoadGameItemsException("No game data or invalid format!")


def _load_items_data(game):
    game.is_debug and log.debug("Load last saved game items")
    items_data = load_data_from_file(PersistenceSettings.settings['items_file'])

    validate_load_data_basic_structure(items_data)
    validate_load_data_game_basic_metadata(items_data)

    if items_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level in game.levels:
        level_data = items_data['game_levels'].get(f"{level.id}")
        if not level_data or not isinstance(level_data['items'], dict):
            continue
        items_level = level_data['items']
        for item in level.items:
            item_data = items_level.get(item.id)
            if not item_data:
                item.kill_hook()
                item.kill()
                continue


def _load_items_not_initial_data(game):
    game.is_debug and log.debug("Load last saved game items: Not initial actors")
    items_data = load_data_from_file(PersistenceSettings.settings['items_new_file'])

    validate_load_data_basic_structure(items_data)
    validate_load_data_game_basic_metadata(items_data)

    if items_data.get('no_saved_game_data'):
        raise LoadGameNoSavedGameDataException(PERSISTENCE_NO_SAVED_GAME_DATA_MSG)

    for level_id, level_data in items_data['game_levels'].items():
        level = game.levels[int(level_id) - 1]
        items = []
        for item_id, item_data in level_data['items'].items():
            if item_data['type'] != ActorType.CLOCK_TIMER_A.name:
                continue
            kwargs_ = {
                'owner': Actor.get_actor(item_data['owner']),
                'time_in_secs': item_data['remaining_time_in_secs'],
                }
            item = Actor.factory(
                items_module,
                item_data['type_name'],
                x=item_data['dx'],
                y=item_data['dy'],
                game=game,
                kwargs=kwargs_,
                )
            item.clock.trigger_method = game.run_explosion_mines_in_current_level
            items.append(item)
        level.add_actors(items)
