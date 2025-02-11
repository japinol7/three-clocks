"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
import os
import sys

from threeclocks.version import version

APP_NAME_SHORT = 'Three Clocks'
APP_TECH_NAME = 'threeclocks'

N_LEVELS = 2

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 900

SCORE_BAR_HEIGHT = 64

LOG_START_APP_MSG = f"Start app {APP_TECH_NAME} version: {version.get_version()}"
LOG_END_APP_MSG = f"End app {APP_TECH_NAME}"

APP_WEBSITE_URL = "https://github.com/japinol7/three-clocks"

LOG_FILE = os.path.join(
    'logs', f"log_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')}.log")
LOG_FILE_UNIQUE = os.path.join('logs', "log.log")
SYS_STDOUT = sys.stdout

LOG_GAME_OVER = "Game over!"
LOG_GAME_BEATEN = "Congrats! You have beaten the game!"

LOG_INPUT_ERROR_PREFIX_MSG = "User input error. "

JSON_INDENT_SIZE = 2

SOUND_FORMAT = 'ogg'
MUSIC_FORMAT = 'ogg'

CURRENT_PATH = '.'
BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
SOUNDS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'snd', SOUND_FORMAT)
MUSIC_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'music')
FONT_DEFAULT_NAME = os.path.join(CURRENT_PATH, 'assets', 'data', 'fonts', 'sans.ttf')
FONT_FIXED_DEFAULT_NAME = os.path.join(
    CURRENT_PATH, 'assets', 'data', 'fonts', 'fixed.ttf')

BM_BACKGROUNDS_FOLDER = os.path.join(BITMAPS_FOLDER, 'backgrounds')
BM_LOGOS_FOLDER = os.path.join(BITMAPS_FOLDER, 'logos')
BM_CLOCKS_FOLDER = os.path.join(BITMAPS_FOLDER, 'clocks')
BM_MINES_FOLDER = os.path.join(BITMAPS_FOLDER, 'mines')
BM_EXPLOSIONS_FOLDER = os.path.join(BITMAPS_FOLDER, 'explosions')
BM_SELECTORS_FOLDER = os.path.join(BITMAPS_FOLDER, 'selectors')
BM_SPECIAL_EFFECTS_FOLDER = os.path.join(BITMAPS_FOLDER, 'special_effects')
BM_LIGHTS_FOLDER = os.path.join(BM_SPECIAL_EFFECTS_FOLDER, 'lights')

MUSIC_BOX = (
    f'three_clocks_song__192b.{MUSIC_FORMAT}',
    )

FILE_NAMES = {
    'im_background': ('background', 'png'),
    'im_screen_help': ('screen_help', 'png'),
    'im_logo_japinol': ('logo_japinol_ld', 'png'),
    'im_help_key': ('help_key', 'png'),
    'bg_blue_t1_big_logo': ('bg_blue_t1_big_logo', 'png'),
    'im_board': ('board', 'png'),
    'im_clocks': ('clock', 'png'),
    'im_mines': ('im_mine', 'png'),
    'explosions': ('explosion', 'png'),
    'im_selectors': ('im_selector', 'png'),
    'im_lights': ('im_light', 'png'),
    'snd_clock_click': ('clock_click', SOUND_FORMAT),
    'snd_mine_click': ('mine_click', SOUND_FORMAT),
    'snd_explosion': ('explosion', SOUND_FORMAT),
    }

UI_THEMES_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'ui_assets', 'themes')
UI_MAIN_THEME_FILE = os.path.join(UI_THEMES_FOLDER, 'main_theme.json')
UI_X_SPACE_BETWEEN_BUTTONS = 116
UI_Y_SPACE_BETWEEN_BUTTONS = 42

ALLOWED_CHARS_ALPHANUM_DASH = (
        [chr(i) for i in range(65, 91)]
        + [chr(i) for i in range(97, 123)]
        + [chr(i) for i in range(48, 58)]
        + ['_', '-']
    )
ALLOWED_CHARS_ALPHANUM_SPACE = ALLOWED_CHARS_ALPHANUM_DASH + [' ']
