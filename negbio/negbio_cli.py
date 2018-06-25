"""
Usage:
    negbio [--verbose] <command> [<args>...]

Options:
    --verbose   Print more information about progress.

The most commonly used git commands are:
    text2bioc
    normalize
    section_split
    ssplit
    parse
    ptb2ud
    dner
    neg
"""
from subprocess import call
import logging
import os
from negbio.cli_utils import parse_args

if __name__ == '__main__':
    args = parse_args(__doc__, version='negbio version 2', options_first=True)
    logging.debug('CWD: %s', os.getcwd())

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'text2bioc':
        exit(call(['python', 'negbio/negbio_text2bioc.py'] + argv))
    elif args['<command>'] == 'normalize':
        exit(call(['python', 'negbio/negbio_normalize.py'] + argv))
    elif args['<command>'] == 'section_split':
        exit(call(['python', 'negbio/negbio_section_split.py'] + argv))
    elif args['<command>'] == 'ssplit':
        exit(call(['python', 'negbio/negbio_ssplit.py'] + argv))
    elif args['<command>'] == 'parse':
        exit(call(['python', 'negbio/negbio_parse.py'] + argv))
    elif args['<command>'] == 'ptb2ud':
        exit(call(['python', 'negbio/negbio_ptb2ud.py'] + argv))
    elif args['<command>'] == 'dner':
        exit(call(['python', 'negbio/negbio_dner.py'] + argv))
    elif args['<command>'] == 'neg':
        exit(call(['python', 'negbio/negbio_neg.py'] + argv))
    elif args['<command>'] in ['help', None]:
        exit(call(['python', 'negbio.py', '--help']))
    else:
        exit("%r is not a negbio.py command. See 'negbio help'." % args['<command>'])
