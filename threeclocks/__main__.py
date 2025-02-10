"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
import logging

from argparse import ArgumentParser
import gc
import traceback
import sys

import pygame as pg

from threeclocks.config.constants import (
    LOG_START_APP_MSG,
    LOG_END_APP_MSG,
    )
from threeclocks.game_entry_point import Game
from threeclocks.tools.logger import logger
from threeclocks.tools.logger.logger import (
    log, LOGGER_FORMAT,
    LOGGER_FORMAT_NO_DATE
    )
from threeclocks.screens import ScreenStartGame


def main():
    """Entry point of The Three Clocks program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="Three Clocks",
                            prog="threeclocks",
                            usage="%(prog)s usage: threeclocks [-h] [-f] [-l] [-m] [-n] [-uu] [-d] [-t]")
    parser.add_argument('-f', '--fullscreen', default=False, action='store_true',
                        help='Full screen display activated when starting the game')
    parser.add_argument('-l', '--multiplelogfiles', default=False, action='store_true',
                        help='A log file by app execution, instead of one unique log file')
    parser.add_argument('-m', '--stdoutlog', default=False, action='store_true',
                        help='Print logs to the console along with writing them to the log file')
    parser.add_argument('-n', '--nologdatetime', default=False, action='store_true',
                        help='Logs will not print a datetime')
    parser.add_argument('-u', default=False, action='store_true',
                        help='u option deactivated')
    parser.add_argument('-uu', '--nodisplayscaled', default=False, action='store_true',
                        help='Remove the scaling of the game screen. '
                             'Resolution depends on desktop size and scale graphics. '
                             'Note that Pygame scaled is considered an experimental API '
                             'and is subject to change.')
    parser.add_argument('-d', '--debug', default=None, action='store_true',
                        help='Debug actions when pressing the right key, information and traces')
    parser.add_argument('-t', '--debugtraces', default=None, action='store_true',
                        help='Show debug back traces information when something goes wrong')
    args = parser.parse_args()

    logger_format = LOGGER_FORMAT_NO_DATE if args.nologdatetime else LOGGER_FORMAT
    args.stdoutlog and logger.add_stdout_handler(logger_format)
    logger.add_file_handler(args.multiplelogfiles, logger_format)
    log.setLevel(logging.INFO)

    pg.init()

    log.info(LOG_START_APP_MSG)
    not args.stdoutlog and print(LOG_START_APP_MSG)
    log.info(f"App arguments: {' '.join(sys.argv[1:])}")

    # Multiple games loop
    while not Game.is_exit_game:
        try:
            Game.new_game = False
            pg.mouse.set_visible(True)
            game = Game(is_debug=args.debug, is_full_screen=args.fullscreen,
                        no_log_datetime=args.nologdatetime,
                        stdout_log=args.stdoutlog,
                        is_no_display_scaled=args.nodisplayscaled)
            Game.ui_manager.set_game_data(game)
            game.screen_start_game = ScreenStartGame(game)
            while game.is_start_screen:
                game.screen_start_game.start_up()
            if not Game.is_exit_game:
                game.start()
                del game.screen_start_game
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'ERROR. Abort execution: {e}')
            not args.stdoutlog and print(f'CRITICAL ERROR. Abort execution: {e}')
            break

    log.info(LOG_END_APP_MSG)
    not args.stdoutlog and print(LOG_END_APP_MSG)
    pg.quit()


if __name__ == '__main__':
    main()
