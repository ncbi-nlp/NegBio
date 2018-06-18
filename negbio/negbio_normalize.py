"""
Usage:
    negbio normalize [options] --out=<directory> <source> ...

Options:
    --suffix=<str>  [default: .normalized.xml]
    --verbose
"""

import os
from pathlib import Path
import docopt
import tqdm
import bioc

from ext.normalize_mimiccxr import normalize_collection
from pipeline.scan import scan_collection

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    scan_collection(source=argv['<source>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                    directory=argv['--out'], fn=normalize_collection)
