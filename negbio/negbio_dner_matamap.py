"""
Detect UMLS concepts

Usage:
    negbio_pipeline dner_mm [options] --metamap=<binary> --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .mm.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --metamap=<binary>      The MetaMap binary
    --cuis=<file>           Specify CUI list
"""

from negbio.cli_utils import parse_args
from negbio.pipeline.dner_mm import run_metamap_col
from negbio.pipeline.scan import scan_collection
from pymetamap import MetaMap


def read_cuis(pathname):
    cuis = set()
    with open(pathname) as fp:
        for line in fp:
            line = line.strip()
            if line:
                cuis.add(line)
    return cuis


if __name__ == '__main__':
    argv = parse_args(__doc__)
    mm = MetaMap.get_instance(argv['--metamap'])

    if argv['--cuis'] is None:
        cuis = None
    else:
        cuis = read_cuis(argv['--cuis'])

    scan_collection(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                    fn=run_metamap_col, non_sequences=[mm, cuis])
