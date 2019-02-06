"""
Detect concepts from vocab

Usage:
    negbio_pipeline dner_chexpert [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>                       Append an additional SUFFIX to file names. [default: .chexpert.xml]
    --output=<directory>                    Specify the output directory.
    --verbose                               Print more information about progress.
    --mention_phrases_dir=<directory>       Directory containing mention phrases for each observation. [default: negbio/chexpert/phrases/mention]
    --unmention_phrases_dir=<directory>     Directory containing unmention phrases  for each observation.  [default: negbio/chexpert/phrases/unmention]
"""
from pathlib2 import Path

from negbio.chexpert.stages.extract import NegBioExtractor
from negbio.cli_utils import parse_args, get_absolute_path
from negbio.pipeline.scan import scan_collection


def run_extractor(collection, extractor):
    """
    Args:
        collection (BioCCollection):
        extractor (NegBioExtractor):
    """
    extractor.extract_all(collection)


if __name__ == '__main__':
    argv = parse_args(__doc__)

    argv = get_absolute_path(argv,
                             '--mention_phrases_dir',
                             'negbio/chexpert/phrases/mention')
    argv = get_absolute_path(argv,
                             '--unmention_phrases_dir',
                             'negbio/chexpert/phrases/unmention')

    extractor = NegBioExtractor(Path(argv['--mention_phrases_dir']),
                                Path(argv['--unmention_phrases_dir']),
                                verbose=argv['--verbose'])
    scan_collection(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                    fn=run_extractor, non_sequences=[extractor])
