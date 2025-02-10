"""Module ui_ingame."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg
import pygame_gui as pgui

from threeclocks.config.constants import (
    ALLOWED_CHARS_ALPHANUM_SPACE,
    UI_Y_SPACE_BETWEEN_BUTTONS,
    UI_MAIN_THEME_FILE,
    )
from threeclocks.ui.ui_main_utils.ui_main_utils import (
    clean_general_ui_items,
    save_game_ui_action,
    save_game_directory_ui_action,
    )


class UIInGame:
    def __init__(self, game):
        self.game = game
        self.manager = pgui.UIManager(game.size, theme_path=UI_MAIN_THEME_FILE)
        self.items = {}

        self._add_items()

    def clean_game_data(self):
        self.game = None

    def set_game_data(self, game):
        self.game = game

    def clean_ui_items(self):
        clean_general_ui_items(self)

    def hide_additional_game_items(self):
        if self.items.get('text_message_window'):
            self.items['text_message_window'].hide()

        self.items['clock_selection_list'].hide()
        self.items['mine_selection_list'].hide()
        self.items['save_game_ok_button'].hide()
        self.items['text_entry_line'].hide()

    def _add_items(self):

        def clocks_action():
            self.hide_additional_game_items()
            clocks = [x.id for x in self.game.level.clocks]
            self.items['clock_selection_list'].set_item_list(clocks)
            self.items['clock_selection_list'].show()

        def mines_action():
            self.hide_additional_game_items()
            mines = [x.id for x in self.game.level.mines]
            self.items['mine_selection_list'].set_item_list(mines)
            self.items['mine_selection_list'].show()

        def continue_game_action():
            self.game.screen_pause.done = True

        def save_game_action():
            save_game_ui_action(self)

        def save_game_directory_action():
            save_game_directory_ui_action(self, persist_game_before_copy=True)

        button_pos_x = 100
        button_pos_y = 470
        button_size = 170, 40

        self.items['clocks_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Clocks",
            manager=self.manager,
            command=clocks_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['mines_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Mines",
            manager=self.manager,
            command=mines_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['continue_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Continue",
            manager=self.manager,
            command=continue_game_action,
            )
        button_pos_y += UI_Y_SPACE_BETWEEN_BUTTONS
        self.items['save_game_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((button_pos_x, button_pos_y), button_size),
            text="Save Game",
            manager=self.manager,
            command=save_game_action,
            )

        self.items['clock_selection_list'] = (pgui.elements.ui_selection_list.
                UISelectionList(
            relative_rect=pg.Rect((296, 430), (220, 275)),
            manager=self.manager,
            item_list = [],
            visible=False,
            ))
        self.items['mine_selection_list'] = (pgui.elements.ui_selection_list.
                UISelectionList(
            relative_rect=pg.Rect((296, 430), (220, 275)),
            manager=self.manager,
            item_list = [],
            visible=False,
            ))
        self.items['text_entry_line'] = (pgui.elements.ui_text_entry_line.
                UITextEntryLine(
            relative_rect=pg.Rect((385, 480), (390, 42)),
            manager=self.manager,
            visible=False,
            ))
        self.items['text_entry_line'].set_allowed_characters(
            ALLOWED_CHARS_ALPHANUM_SPACE)

        self.items['save_game_ok_button'] = pgui.elements.UIButton(
            relative_rect=pg.Rect((495, 524), (170, 40)),
            text="Save Named Game",
            manager=self.manager,
            command=save_game_directory_action,
            visible=False,
            )
