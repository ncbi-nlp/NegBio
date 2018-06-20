"""
Parse sentences

Usage:
    negbio parse [options] --output=<directory> <file> ...

Options:
    --model=<directory>     Bllip parser model directory.
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .bllip.xml]
    --verbose               Print more information about progress.
"""

from negbio.cli_utils import parse_args
from negbio.pipeline.parse import parse, Bllip
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    parser = Bllip(model_dir=argv['--model'])
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=parse, non_sequences=[parser])
