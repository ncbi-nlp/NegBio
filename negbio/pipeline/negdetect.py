"""
Detect negation and uncertainty

Usage:
    neg [options] --out=DIRECTORY SOURCE ...

Options:
    --neg-patterns=FILE             negation rules [default: patterns/neg_patterns.txt]
    --uncertainty-patterns=FILE     uncertainty rules [default: patterns/uncertainty_patterns.txt]
"""

from __future__ import print_function

import logging
import re
import sys

import docopt

from negbio.neg.neg_detector import Detector
from negbio.pipeline import scan


def neg_mesh(annotations):
    """
    Detect negative MeSH
    """
    for ann in annotations:
        if ann.infons.get('CUI', None) == 'C0332125':
            ann.infons[Detector.NEGATION] = 'True'


def uncertain_mesh(annotations):
    """
    Detect uncertain MeSH
    """
    for ann in annotations:
        if ann.infons.get('CUI', None) == 'C0332148':
            ann.infons[Detector.UNCERTAINTY] = 'True'


def is_neg_regex(text):
    if re.search(r'^(findings|impression): no ', text, re.I):
        return True
    return False


def _mark_anns(annotations, begin, end, type):
    """Mark all annotations in [begin:end] as type"""
    for ann in annotations:
        total_loc = ann.get_total_location()
        if begin <= total_loc.offset and total_loc.offset + total_loc.length < end:
            ann.infons[type] = 'True'


def _extend(document, type):
    def _is_type(annotation):
        return annotation.infons.get(type, None) == 'True'

    neg_anns = []
    for passage in document.passages:
        for ann in passage.annotations:
            if _is_type(ann):
                neg_anns.append(ann)

    for passage in document.passages:
        for ann in passage.annotations:
            if not _is_type(ann):
                for nann in neg_anns:
                    if ann in nann:
                        ann.infons[type] = 'True'
                        break
                    if nann in ann and 'CUI' in ann and 'CUI' in nann and ann.infons['CUI'] == nann.infons['CUI']:
                        ann.infons[type] = 'True'
                        break


def detect(document, detector):
    """
    Args:
        document(BioCDocument):
        detector(Detector): detector. Define customized patterns in the detector
    """
    logger = logging.getLogger(__name__)

    try:

        for passage in document.passages:
            neg_mesh(passage.annotations)
            uncertain_mesh(passage.annotations)

            locs = []
            for ann in passage.annotations:
                total_loc = ann.get_total_location()
                locs.append((total_loc.offset, total_loc.offset+total_loc.length))

            for sentence in passage.sentences:
                if is_neg_regex(sentence.text):
                    _mark_anns(passage.annotations, sentence.offset, sentence.offset + len(sentence.text), Detector.NEGATION)
                    continue
                for name, matcher, loc in detector.detect(sentence, locs):
                    logging.debug('Find: %s, %s, %s', name, matcher.pattern, loc)
                    _mark_anns(passage.annotations, loc[0], loc[1], name)

        # _extend(document, Detector.NEGATION)
        # _extend(document, Detector.UNCERTAINTY)
    except:
        logger.exception("Cannot process %s", document.id)
    return document


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    neg_detector = Detector(argv['--neg-patterns'], argv['--uncertainty-patterns'])
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix='.neg.xml',
                       fn=detect, non_sequences=[neg_detector])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    main(sys.argv[1:])
