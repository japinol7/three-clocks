"""Module utils."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Size = namedtuple('Size', ['w', 'h'])


def pretty_dict_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent, f"{str(key):22}", '-->', end='')
        if isinstance(value, dict):
            print('')
            pretty_dict_print(value, indent + 1)
        else:
            print('\t' * (indent + 1), '{:>10}'.format(str(value)))


def pretty_dict_to_string(d, indent=0, with_last_new_line=False, res='', first_time=True):
    for key, value in d.items():
        res = '%s%s%s%s' % (res, '\t' * indent, f"{str(key):28}", '-->')
        if isinstance(value, dict):
            res = '%s\n' % res
            res = '%s%s' % (res, pretty_dict_to_string(value, indent + 1, res='', first_time=False))
        else:
            res = '{}{}{:>10}\n'.format(res, '\t' * (indent + 1), str(value))
    if first_time and not with_last_new_line:
        res = res[:-1]
    return res
