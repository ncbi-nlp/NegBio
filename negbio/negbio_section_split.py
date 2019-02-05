"""
Split the report into sections based on titles.

Usage:
    negbio_pipeline section_split [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .secsplit.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --pattern=<file>        Specify section title list for matching.
"""
import re

from negbio.cli_utils import parse_args
from negbio.pipeline.scan import scan_document
from negbio.pipeline.section_split import split_document


def read_section_titles(pathname):
    with open(pathname) as fp:
        return re.compile('|'.join(fp.readlines()), re.MULTILINE)


if __name__ == '__main__':
    argv = parse_args(__doc__)

    if argv['--pattern'] is None:
        patterns = None
    else:
        patterns = read_section_titles(argv['--pattern'])

    scan_document(source=argv['<file>'], verbose=argv['--verbose'], suffix=argv['--suffix'],
                  directory=argv['--output'], fn=split_document, non_sequences=[patterns])
