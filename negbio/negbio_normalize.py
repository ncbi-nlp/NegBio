"""
Usage:
    negbio normalize [options] --out=<directory> <source> ...

Options:
    --suffix=<str>  [default: .normalized.xml]
    --verbose
"""

import docopt

from ext.normalize_mimiccxr import normalize
from pipeline.scan import scan_document

if __name__ == '__main__':
    argv = docopt.docopt(__doc__)

    scan_document(source=argv['<source>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                  directory=argv['--out'], fn=normalize)
