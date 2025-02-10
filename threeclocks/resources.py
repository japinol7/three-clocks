"""Module resources."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from threeclocks.tools.utils.colors import Color
from threeclocks.config import constants as consts
from threeclocks.tools.utils import utils_graphics as libg_jp
from threeclocks.config.settings import Settings


def file_name_get(name, subname='', folder=consts.BITMAPS_FOLDER):
    return os.path.join(
        folder,
        f"{consts.FILE_NAMES['%s%s' % (name, subname)][0]}"
        f".{consts.FILE_NAMES['%s%s' % (name, subname)][1]}")


class Resource:
    """Some resources used in the game that do not have their own class."""
    clock_click_sound = None
    mine_click_sound = None
    explosion_sound = None
    images = {}
    txt_surfaces = {
        'game_paused': None, 'player_wins': None,
        'game_over': None, 'game_over_2': None,
        'press_intro_to_continue_center': None,
        'press_intro_to_continue': None, 'press_intro_to_continue_2': None,
        'game_start': None, 'game_start_2': None,
        'congrats': None, 'congrats_2': None,
        'you_have_beaten_the_game': None, 'you_have_beaten_the_game_2': None,
        }

    @classmethod
    def load_sound_resources(cls):
        file_name = file_name_get(name='snd_clock_click', folder=consts.SOUNDS_FOLDER)
        try:
            cls.clock_click_sound = pg.mixer.Sound(file_name)
        except Exception as e:
            raise Exception(
                f"{e} SDL Error. Probably no sound device found. "
                f"Connect your headphones and it should work")

        cls.mine_click_sound = pg.mixer.Sound(
            file_name_get(name='snd_mine_click', folder=consts.SOUNDS_FOLDER))

    @classmethod
    def render_text_frequently_used(cls, game):
        libg_jp.render_text('– PAUSED –', 204 + Settings.screen_width // 2,
                            Settings.screen_height // 4.6,
                            cls.txt_surfaces, 'game_paused', color=Color.CYAN,
                            size=70, align="center")

        libg_jp.render_text('– Press Escape to Exit this Game  –', Settings.screen_width // 2,
                            (Settings.screen_height // 2.6) - 6,
                            cls.txt_surfaces, 'exit_current_game_confirm', color=Color.CYAN,
                            size=78, align="center")

        libg_jp.render_text('– Press Ctrl + Enter to Continue –', Settings.screen_width // 2,
                            (Settings.screen_height // 1.764) + 82,
                            cls.txt_surfaces, 'press_intro_to_continue_center', color=Color.CYAN,
                            size=82, align="center")

        libg_jp.render_text('– Press Ctrl + Enter to Continue –', Settings.screen_width // 1.992,
                            Settings.screen_height // 1.286,
                            cls.txt_surfaces, 'press_intro_to_continue', color=Color.BLUE,
                            size=68, align="center")
        libg_jp.render_text('– Press Ctrl + Enter to Continue –', Settings.screen_width // 2,
                            Settings.screen_height // 1.290,
                            cls.txt_surfaces, 'press_intro_to_continue_2', color=Color.CYAN,
                            size=68, align="center")

        libg_jp.render_text("KUDOS", Settings.screen_width // 1.99,
                            Settings.screen_height // 2.484,
                            cls.txt_surfaces, 'congrats', color=Color.BLUE,
                            size=146, align="center")
        libg_jp.render_text("KUDOS", Settings.screen_width // 2,
                            Settings.screen_height // 2.5,
                            cls.txt_surfaces, 'congrats_2', color=Color.CYAN,
                            size=146, align="center")

        libg_jp.render_text('You have beaten the game', Settings.screen_width // 1.991,
                            Settings.screen_height // 1.75,
                            cls.txt_surfaces, 'you_have_beaten_the_game', color=Color.BLUE,
                            size=85, align="center")
        libg_jp.render_text('You have beaten the game', Settings.screen_width // 2,
                            Settings.screen_height // 1.755,
                            cls.txt_surfaces, 'you_have_beaten_the_game_2', color=Color.CYAN,
                            size=85, align="center")

        libg_jp.render_text("GAME OVER", Settings.screen_width // 1.99,
                            Settings.screen_height // 2.484,
                            cls.txt_surfaces, 'game_over', color=Color.BLUE,
                            size=140, align="center")
        libg_jp.render_text("GAME OVER", Settings.screen_width // 2,
                            Settings.screen_height // 2.5,
                            cls.txt_surfaces, 'game_over_2', color=Color.CYAN,
                            size=140, align="center")

    @classmethod
    def load_and_render_background_images(cls):
        """Load and render background images and effects."""
        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_background', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['background'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='bg_blue_t1_big_logo', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_blue_t1'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name='im_screen_help', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['screen_help'] = img

        img = pg.image.load(file_name_get(folder=consts.BM_BACKGROUNDS_FOLDER,
                                          name=Settings.im_bg_start_game)).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['screen_start'] = img

        img = pg.image.load(file_name_get(name='im_help_key')).convert()
        img = pg.transform.smoothscale(
            img,
            (Settings.help_key_size.w,
            Settings.help_key_size.h))
        cls.images['help_key'] = img

        img = pg.image.load(file_name_get(
            folder=consts.BM_LOGOS_FOLDER, name='im_logo_japinol')).convert()
        img = pg.transform.smoothscale(img, (108, 20))
        cls.images['logo_jp'] = img

        img = pg.image.load(file_name_get(name='im_board')).convert_alpha()
        cls.images['board'] = img
        Settings.board_width = Resource.images['board'].get_width()
        Settings.board_height = Resource.images['board'].get_height()
        Settings.board_x = Settings.board_base_x - Settings.board_width // 2 \
                           + Settings.board_base_width // 2
        Settings.board_y = Settings.board_base_y - Settings.board_height // 2 \
                           + Settings.board_base_height // 2

    @classmethod
    def load_and_render_scorebar_images_and_txt(cls):
        libg_jp.render_text(
            'XP:', Settings.score_pos_score1[0], Settings.screen_bar_near_top + 1,
                cls.txt_surfaces, 'sb_score_title1', color=Color.CYAN)
        libg_jp.render_text(
            'Level:', Settings.score_pos_level[0], Settings.screen_bar_near_top + 1,
            cls.txt_surfaces, 'sb_level', color=Color.CYAN)

    @staticmethod
    def load_music_song(current_song):
        pg.mixer.music.load(os.path.join(consts.MUSIC_FOLDER, consts.MUSIC_BOX[current_song]))
