"""
Detect concepts from vocab

Usage:
    negbio dner_chexpert [options] --output=<directory> <file> ...

Options:
    --suffix=<suffix>                       Append an additional SUFFIX to file names. [default: .chexpert.xml]
    --output=<directory>                    Specify the output directory.
    --verbose                               Print more information about progress.
    --mention_phrases_dir=<directory>       Directory containing mention phrases for each observation. [default: negbio/chexpert/phrases/mention]
    --unmention_phrases_dir=<directory>     Directory containing unmention phrases  for each observation.  [default: negbio/chexpert/phrases/unmention]
"""
import itertools
import re

from bioc import biocitertools
from pathlib2 import Path

from negbio.chexpert.stages import Extractor
from negbio.cli_utils import parse_args
from negbio.pipeline.scan import scan_collection


def run_cheXpert_extractor(collection, extractor):
    """Extract the observations in each report.

    Args:
        collection (BioCCollection): Impression passages of each report.

    Return:
        extracted_mentions
    """

    # The BioCCollection consists of a series of documents.
    # Each document is a report (just the Impression section
    # of the report.)
    annotation_index = itertools.count()
    for doc in collection.documents:
        for passage in doc.passages:
            for sentence in passage.sentences:
                obs_phrases = extractor.observation2mention_phrases.items()
                for observation, phrases in obs_phrases:
                    for phrase in phrases:
                        matches = re.finditer(phrase, sentence.text)
                        for match in matches:
                            start, end = match.span(0)
                            if extractor.overlaps_with_unmention(sentence, observation, start, end):
                                continue
                            extractor.add_match(passage, sentence, str(next(annotation_index)), phrase,
                                                observation, start, end)


def run_extractor(collection, extractor):
    extractor.extract(collection)


if __name__ == '__main__':
    argv = parse_args(__doc__)
    extractor = Extractor(Path(argv['--mention_phrases_dir']),
                          Path(argv['--unmention_phrases_dir']),
                          verbose=argv['--verbose'])
    scan_collection(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                    fn=run_cheXpert_extractor, non_sequences=[extractor])
