"""Module settings."""
__author__ = 'Joan A. Pinol  (japinol)'

from threeclocks.tools.utils import utils
from threeclocks.config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    )

FPS_DEFAULT = 64  # Recommended: 64
FPS_MIN = 25
FPS_MAX = 92

CELL_DEFAULT_SIZE = 14

DEFAULT_MUSIC_VOLUME = 0.5


class Settings:
    """Settings of the game."""
    screen_width = None
    screen_height = None
    board_base_x = None
    board_base_y = None
    board_base_width = None
    board_base_height = None
    board_base_center = None
    board_x = None
    board_y = None
    board_width = None
    board_height = None
    screen_aspect_ratio = None
    screen_height_adjusted = None
    screen_width_adjusted = None
    display_start_width = None    # max. width of the user's initial display mode
    display_start_height = None   # max. height of the user's initial display mode
    cell_size = None
    fps = None
    fps_paused = None
    has_selector_no_light = False
    is_full_screen = False
    im_screen_help = None
    im_bg_start_game = None
    score_to_win = None
    screen_near_top = None
    screen_near_bottom = None
    screen_near_right = None
    grid_width = None
    grid_height = None
    screen_bar_near_top = None
    sprite_health_bar_pos_rel = None   # Relative position for sprite health bar
    sprite_health_bar_size = None
    font_size1 = None
    font_size2 = None
    font_spc_btn_chars1 = None
    font_spc_btn_chars2 = None
    # scores tuple with label and value x positions
    score_pos_door_keys = None
    score_pos_label = None
    score_pos_x = None
    score_pos_score1 = None
    score_pos_level = None
    logo_jp_std_size = None
    help_key_size = None
    help_key_pos_factor = None
    text_y_distance = None

    @classmethod
    def clean(cls):
        cls.screen_width = SCREEN_WIDTH
        cls.screen_height = SCREEN_HEIGHT
        cls.screen_aspect_ratio = cls.screen_width / cls.screen_height
        cls.screen_height_adjusted = None
        cls.screen_width_adjusted = None
        cls.board_base_x = 552
        cls.board_base_y = 50
        cls.board_base_width = 843
        cls.board_base_height = 725
        cls.board_base_center = (
            Settings.board_base_x + Settings.board_base_width // 2,
            Settings.board_base_y + Settings.board_base_height // 2)
        cls.board_x = None
        cls.board_y = None
        cls.board_width = None
        cls.board_height = None
        cls.cell_size = CELL_DEFAULT_SIZE
        cls.cell_size_ratio = cls.screen_width * cls.screen_height / CELL_DEFAULT_SIZE
        cls.fps = FPS_DEFAULT
        cls.fps_paused = 16
        cls.has_selector_no_light = False
        cls.is_full_screen = False
        cls.im_screen_help = 'im_screen_help'
        cls.im_bg_start_game = 'im_background'
        cls.screen_near_top = None
        cls.screen_near_bottom = None
        cls.screen_near_right = None
        cls.grid_width = None
        cls.grid_height = None
        cls.screen_bar_near_top = None
        cls.font_size1 = None
        cls.font_size2 = None
        cls.font_spc_btn_chars1 = None
        cls.font_spc_btn_chars2 = None
        # scores tuple with label and value x positions
        cls.logo_jp_std_size = utils.Size(w=244, h=55)
        cls.help_key_pos = 1404, 14
        cls.help_key_size = utils.Size(w=124, h=30)
        cls.score_pos_score1 = [322, 380]
        cls.score_pos_level = [1100, 1175]
        cls.score_pos_label = 15, 70
        cls.score_pos_x = 230
        cls.text_y_distance = 30
        cls.log_to_file = True

    @classmethod
    def calculate_settings(cls, full_screen=None):
        cls.clean()

        # Define screen values to resize the screen and images if necessary
        cls.screen_width_adjusted = int(cls.screen_height * cls.screen_aspect_ratio)
        cls.screen_height_adjusted = cls.screen_height

        # Set full screen or windowed screen
        cls.is_full_screen = True if full_screen else False

        # Set positions for images and text
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.screen_near_bottom = cls.screen_height - cls.cell_size + 1
        cls.screen_near_right = cls.screen_width - cls.cell_size + 1
        cls.screen_bar_near_top = 15

        # Font sizes for scores, etc
        cls.font_size1 = 22
        cls.font_size2 = 34
        cls.font_spc_btn_chars1 = 15
        cls.font_spc_btn_chars2 = 21

        cls.screen_near_top = int(cls.screen_height * 0.057)
        cls.screen_near_top = int(cls.screen_near_top * 2)
