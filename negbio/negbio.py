"""
Usage:
    negbio [--verbose] <command> [<args>...]

Options:
    --verbose
"""

import logging
from subprocess import call

import docopt


def get_args(args):
    s = ''
    for k in args:
        s += '    {}: {}\n'.format(k, args[k])
    return s


if __name__ == '__main__':
    args = docopt.docopt(__doc__,
                         version='negbio version 2',
                         options_first=True)

    if args['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug('global arguments:\n%s', get_args(args))

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'text2bioc':
        exit(call(['python', 'negbio/negbio_text2bioc.py'] + argv))
    elif args['<command>'] == 'normalize':
        exit(call(['python', 'negbio/negbio_normalize.py'] + argv))
    elif args['<command>'] == 'section_split':
        exit(call(['python', 'negbio/negbio_section_split.py'] + argv))
    elif args['<command>'] in ['help', None]:
        exit(call(['python', 'negbio.py', '--help']))
    else:
        exit("%r is not a negbio.py command. See 'negbio help'." % args['<command>'])