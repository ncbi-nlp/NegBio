import logging

import docopt


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