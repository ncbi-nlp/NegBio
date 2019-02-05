"""
Usage:
    negbio_pipeline normalize [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .normalized.xml]
    --verbose               Print more information about progress.
"""

from negbio.cli_utils import parse_args
from negbio.ext.normalize_mimiccxr import normalize
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    scan_document(source=argv['<file>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                  directory=argv['--output'], fn=normalize)
