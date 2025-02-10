"""Module utils_graphics."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from threeclocks.tools.utils.colors import Color
from threeclocks.config import constants as consts
from threeclocks.config.settings import Settings


FONT_DEFAULT_FIXED = False
chars_render = {}
chars_fixed_render = {}


def full_screen_switch(game):
    Settings.is_full_screen = not Settings.is_full_screen
    game.screen = pg.display.set_mode(
        game.size,
        Settings.is_full_screen and game.full_screen_flags or game.normal_screen_flags)


def draw_text(text, x, y, screen, font_name=consts.FONT_DEFAULT_NAME, size=None,
              color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)


def draw_image(x, y, screen, surface_dic, surface_name, file_name, align="topleft",
               width=None, height=None, alpha_color=None):
    image = pg.image.load((os.path.join(consts.BITMAPS_FOLDER, file_name))).convert()
    if width and height:
        image = pg.transform.smoothscale(image, (width, height))
    if alpha_color:
        image.set_colorkey(alpha_color)
    rect = image.get_rect(**{align: (x, y)})
    surface_dic[surface_name] = (image, rect)
    screen.blit(image, rect)


def render_text(text, x, y, surface_dic, surface_name, font_name=consts.FONT_DEFAULT_NAME,
                size=None, color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface_dic[surface_name] = (text_surface, text_rect)


def render_text_tuple(text, x, y, surface_dic, surface_name, font_name=consts.FONT_FIXED_DEFAULT_NAME,
                      size=None, color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface_dic[(surface_name, color)] = (text_surface, text_rect)


def chars_render_text_tuple(font_name=consts.FONT_FIXED_DEFAULT_NAME):
    ch_render = chars_render if font_name != consts.FONT_FIXED_DEFAULT_NAME else chars_fixed_render
    char_code_list = [x for x in range(32, 126)]
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.GREEN, font_name=font_name)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.CYAN, font_name=font_name)


def draw_text_rendered(text, x, y, screen, color, is_font_fixed=False,
                       space_btw_chars=None, space_btw_words=None):
    ch_render = chars_render if not is_font_fixed else chars_fixed_render
    if not space_btw_chars:
        space_btw_chars = Settings.font_spc_btn_chars1
    xx = x
    for ch in text:
        if not ch_render.get((ord(ch), color)):
            ch = '-'
        screen.blit(ch_render[(ord(ch), color)][0], (xx, y))
        if ch != ' ':
            xx += space_btw_chars
        else:
            if space_btw_words:
                xx += space_btw_words
            else:
                xx += space_btw_chars // 3


def draw_text_multi_lines_rendered(
        text, x, y, screen, color, is_font_fixed=False,
        space_btw_chars=None, space_btw_words=None, space_btw_lines=None):

    for i, txt in enumerate(text.splitlines()):
        ch_render = chars_render if not is_font_fixed else chars_fixed_render
        if not space_btw_chars:
            space_btw_chars = Settings.font_spc_btn_chars1
        xx = x
        for ch in txt:
            if not ch_render.get((ord(ch), color)):
                ch = '-'
            screen.blit(ch_render[(ord(ch), color)][0], (xx, y + (space_btw_lines * i)))
            if ch != ' ':
                xx += space_btw_chars
            else:
                if space_btw_words:
                    xx += space_btw_words
                else:
                    xx += space_btw_chars // 3


def point_to_str(point):
    return f"{point[0]};{point[1]}"


def str_to_point(string):
    return [int(v) for v in string.split(";")[:2]]


def set_mask_alpha(surface, alpha_color):
    return multiply_color_on_surface(surface, alpha_color)


def multiply_color_on_surface(surface, color):
    base_surface = surface.copy()
    base_surface.fill(color)
    new_surface = surface.copy()
    new_surface.blit(base_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return new_surface


def get_chunk(point, chunk_size):
    return [point[0] // chunk_size, point[1] // chunk_size]


def draw_grid(screen, cell_size, screen_width, screen_height, screen_near_top, color):
    for x in range(0, screen_width, cell_size):
        pg.draw.line(screen, color, (x, screen_near_top), (x, screen_height))
    for y in range(screen_near_top, screen_height, cell_size):
        pg.draw.line(screen, color, (0, y), (screen_width, y))
