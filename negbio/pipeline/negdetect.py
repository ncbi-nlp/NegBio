import logging
import re

from negbio.neg.neg_detector import Detector


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
        if begin <= total_loc.offset and total_loc.offset + total_loc.length <= end:
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
    try:

        for passage in document.passages:
            neg_mesh(passage.annotations)
            uncertain_mesh(passage.annotations)

            locs = []
            for ann in passage.annotations:
                total_loc = ann.get_total_location()
                locs.append((total_loc.offset, total_loc.offset + total_loc.length))

            for sentence in passage.sentences:
                if is_neg_regex(sentence.text):
                    _mark_anns(passage.annotations, sentence.offset, sentence.offset + len(sentence.text),
                               Detector.NEGATION)
                    continue
                for name, matcher, loc in detector.detect(sentence, locs):
                    logging.debug('Find: %s, %s, %s', name, matcher.pattern, loc)
                    _mark_anns(passage.annotations, loc[0], loc[1], name)

        # _extend(document, Detector.NEGATION)
        # _extend(document, Detector.UNCERTAINTY)
    except:
        logging.exception("Cannot process %s", document.id)
    return document
