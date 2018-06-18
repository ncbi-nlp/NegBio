"""
Parse sentences

Usage:
    negbio parse [options] --out=DIRECTORY SOURCE ...

Options:
    --model=MODEL_DIR   Bllip parser model directory
    --suffix=<str>      [default: .bllip.xml]
    --verbose
"""
import logging

import docopt

from pipeline import scan
from pipeline.parse import parse, Bllip

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    parser = Bllip(model_dir=argv['--model'])
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix=argv['--suffix'],
                       fn=parse, non_sequences=[parser])
