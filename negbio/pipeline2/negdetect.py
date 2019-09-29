import logging
import re

from negbio.neg.neg_detector import Detector
from negbio.pipeline2.pipeline import Pipe


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


def _mark_anns(annotations, begin, end, type, pattern):
    """Mark all annotations in [begin:end] as type"""
    for ann in annotations:
        total_loc = ann.total_span
        if begin <= total_loc.offset and total_loc.offset + total_loc.length <= end:
            ann.infons[type] = 'True'
            if 'pattern' in pattern:
                ann.infons['pattern'] = str(pattern['pattern'])
            if 'id' in pattern:
                ann.infons['pattern_id'] = pattern['id']


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
                    if nann in ann and 'CUI' in ann.infons and 'CUI' in nann.infons \
                            and ann.infons['CUI'] == nann.infons['CUI']:
                        ann.infons[type] = 'True'
                        break


class NegBioNegDetector(Pipe):
    def __init__(self, detector):
        self.detector = detector

    def __call__(self, doc, *args, **kwargs):
        try:
            for passage in doc.passages:
                neg_mesh(passage.annotations)
                uncertain_mesh(passage.annotations)

                locs = []
                for ann in passage.annotations:
                    total_loc = ann.total_span
                    locs.append((total_loc.offset, total_loc.offset + total_loc.length))

                sentence_locs_map = {}
                for sentence in passage.sentences:
                    start = sentence.offset
                    end = start + len(sentence.text)
                    sublocs = [l for l in locs if start <= l[0] <= end]
                    if len(sublocs) != 0:
                        sentence_locs_map[sentence] = sublocs

                for sentence, sublocs in sentence_locs_map.items():
                    if is_neg_regex(sentence.text):
                        _mark_anns(passage.annotations, sentence.offset,
                                   sentence.offset + len(sentence.text),
                                   Detector.NEGATION,
                                   {'id': 'neg regular expression',
                                    'pattern': r'^(findings|impression): no '})
                        continue
                    for name, matcher, loc in self.detector.detect(sentence, sublocs):
                        if matcher is None:
                            _mark_anns(passage.annotations, loc[0], loc[1], name,
                                       {'id': 'neg regular expression',
                                        'pattern': 'neg graph'})
                        else:
                            logging.debug('Find: %s, %s, %s', name, matcher.pattern, loc)
                            if matcher.pattern not in self.detector.total_patterns:
                                _mark_anns(passage.annotations, loc[0], loc[1], name,
                                           {'id': 'missing patterns',
                                            'pattern': str(matcher.pattern)})
                            else:
                                _mark_anns(passage.annotations, loc[0], loc[1], name,
                                           self.detector.total_patterns[matcher.pattern])

            # _extend(document, Detector.NEGATION)
            # _extend(document, Detector.UNCERTAINTY)
        except:
            logging.exception("Cannot process %s", doc.id)
        return doc
