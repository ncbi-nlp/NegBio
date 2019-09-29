"""
Detect UMLS concepts

Usage:
    negbio_dner_mm [options] --metamap=<binary> --output=<directory> <file> ...

Options:
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .mm.xml]
    --output=<directory>    Specify the output directory.
    --verbose               Print more information about progress.
    --metamap=<binary>      The MetaMap binary
    --cuis=<file>           Specify CUI list
    --overwrite             Overwrite the output file.
"""

from negbio.cli_utils import parse_args
from negbio.pipeline2.dner_mm import MetaMapExtractor
from negbio.pipeline2.pipeline import NegBioPipeline
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

    extractor = MetaMapExtractor(mm, cuis)
    pipeline = NegBioPipeline(pipeline=[('MetaMapExtractor', extractor)])
    pipeline.scan(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  overwrite=argv['--overwrite'])
