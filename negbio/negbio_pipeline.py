"""
Usage:
    negbio_pipeline [--verbose] <command> [<args>...]

Options:
    --verbose   Print more information about progress.

The most commonly used negbio commands are:
    text2bioc
    normalize
    section_split
    ssplit
    parse
    ptb2ud
    dner_mm
    dner_chexpert
    neg
    neg_chexpert
    cleanup
"""
from subprocess import call
import logging
import os
from negbio.cli_utils import parse_args


def main():
    args = parse_args(__doc__, version='negbio version 2', options_first=True)
    logging.debug('CWD: %s', os.getcwd())

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'text2bioc':
        exit(call(['python', '-m', 'negbio.negbio_text2bioc'] + argv))
    elif args['<command>'] == 'normalize':
        exit(call(['python', '-m', 'negbio.negbio_normalize'] + argv))
    elif args['<command>'] == 'section_split':
        exit(call(['python', '-m', 'negbio.negbio_section_split'] + argv))
    elif args['<command>'] == 'ssplit':
        exit(call(['python', '-m', 'negbio.negbio_ssplit'] + argv))
    elif args['<command>'] == 'parse':
        exit(call(['python', '-m', 'negbio.negbio_parse'] + argv))
    elif args['<command>'] == 'ptb2ud':
        exit(call(['python', '-m', 'negbio.negbio_ptb2ud'] + argv))
    elif args['<command>'] == 'dner_mm':
        exit(call(['python', '-m', 'negbio.negbio_dner_matamap'] + argv))
    elif args['<command>'] == 'dner_chexpert':
        exit(call(['python', '-m', 'negbio.negbio_dner_chexpert'] + argv))
    elif args['<command>'] == 'neg':
        exit(call(['python', '-m', 'negbio.negbio_neg'] + argv))
    elif args['<command>'] == 'neg_chexpert':
        exit(call(['python', '-m', 'negbio.negbio_neg_chexpert'] + argv))
    elif args['<command>'] == 'cleanup':
        exit(call(['python', '-m', 'negbio.negbio_clean'] + argv))
    elif args['<command>'] in ['help', None]:
        exit(call(['python', '-m', 'negbio.negbio_pipeline', '--help']))
    else:
        exit("%r is not a negbio command. See 'negbio help'." % args['<command>'])


if __name__ == '__main__':
    main()
