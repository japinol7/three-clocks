"""Module help_info."""
__author__ = 'Joan A. Pinol  (japinol)'


class HelpInfo:
    """Manages information used for help."""

    @staticmethod
    def print_help_keys():
        print('  F1: \t show a help screen while playing the game'
              '  ^p: \t pause\n'
              ' ESC: exit game\n'
              '  Alt + Enter: change full screen / normal screen mode\n'
              '  ^h: \t shows this help\n'
              )
