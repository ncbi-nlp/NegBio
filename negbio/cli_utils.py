import logging
import os

import docopt


__root__ = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))


def get_args(args):
    s = ''
    for k in args:
        s += '    {}: {}\n'.format(k, args[k])
    return s


def parse_args(doc, **kwargs):
    argv = docopt.docopt(doc, **kwargs)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Arguments:\n%s', get_args(argv))
    return argv


def get_absolute_path(argv, key, default_value):
    print (__root__)
    if argv[key] == default_value:
        argv[key] = os.path.join(__root__, argv[key])
    return argv