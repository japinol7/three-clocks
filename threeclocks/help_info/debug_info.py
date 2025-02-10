"""Module debug_info."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime
from collections import OrderedDict

from threeclocks.tools.logger.logger import log
from threeclocks.tools.utils.utils import pretty_dict_to_string


class DebugInfo:

    def __init__(self, game):
        self.game = game

    @staticmethod
    def print_help_keys():
        print('  ^ numpad_divide: \t interactive debug output\n'
              '  ^d: \t print debug information to console\n'
              )

    def print_debug_info(self):
        debug_dict = OrderedDict([
            ('Time', "No datetime" if self.game.no_log_datetime else str(datetime.now())),
            ('---------', '-------------'),
        ])
        debug_info_title = 'Current game stats:'
        debug_info = f"{debug_info_title}\n"

        debug_info = f"{debug_info}{pretty_dict_to_string(debug_dict, with_last_new_line=True)}" \
                     f"{'-' * 62}"
        log.info(debug_info)
