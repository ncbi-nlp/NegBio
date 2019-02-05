"""
Clean up sentences

Usage:
    negbio_pipeline cleanup [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>               Append an additional SUFFIX to file names. [default: .negbio.xml]
    --verbose                       Print more information about progress.
    --output=<directory>            Specify the output directory.
"""

from negbio.cli_utils import parse_args
from negbio.pipeline.cleanup import clean_sentences
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=clean_sentences)
