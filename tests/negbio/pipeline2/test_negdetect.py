from pathlib import Path

import bioc

import negbio
from negbio.neg.neg_detector import Detector
from negbio.pipeline2.negdetect import NegBioNegDetector, is_neg_regex, _extend
from negbio.pipeline2.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc

__project_dir = Path(negbio.__file__).parent.parent

neg_pattern_file = __project_dir / 'patterns/neg_patterns2.yml'

uncertainty_pattern_file = __project_dir / 'patterns/uncertainty_patterns.yml'

detector = NegBioNegDetector(Detector(
    neg_pattern_file=neg_pattern_file,
    uncertainty_pattern_file=uncertainty_pattern_file,
))


def _get_document(text, tree, sen_ann_index):
    d = text_to_bioc([text], type='d/p/s')
    d.passages[0].sentences[0].infons['parse tree'] = tree
    c = NegBioPtb2DepConverter()
    c.__call__(d)
    d.passages[0].add_annotation(d.passages[0].sentences[0].annotations[sen_ann_index])
    return d


def test_detect():
    text = 'No pneumothorax.'
    tree = '(S1 (S (S (NP (DT No) (NN pneumothorax))) (. .)))'
    d = _get_document(text, tree, 1)
    detector.__call__(d)
    assert d.passages[0].annotations[0].infons['negation'] == 'True'


def test_neg_regex():
    text = 'findings: no pneumothorax.'
    assert is_neg_regex(text)

    d = text_to_bioc([text], type='d/p/s')
    a = bioc.BioCAnnotation()
    a.text = 'pneumothorax'
    a.add_location(bioc.BioCLocation(13, 12))
    d.passages[0].add_annotation(a)
    detector.__call__(d)
    assert d.passages[0].annotations[0].infons['negation'] == 'True'


def test_extend():
    text = 'findings: no pneumothorax.'
    d = text_to_bioc([text], type='d/p/s')
    a = bioc.BioCAnnotation()
    a.text = 'pneumothorax'
    a.add_location(bioc.BioCLocation(13, 12))
    d.passages[0].add_annotation(a)
    detector.__call__(d)

    # fake ann
    a = bioc.BioCAnnotation()
    a.text = 'eumothor'
    a.add_location(bioc.BioCLocation(15, 8))
    d.passages[0].add_annotation(a)

    a = bioc.BioCAnnotation()
    a.text = 'foo'
    a.add_location(bioc.BioCLocation(27, 3))
    d.passages[0].add_annotation(a)

    _extend(d, 'negation')

    assert d.passages[0].annotations[1].infons['negation'] == 'True'
    assert 'negation' not in d.passages[0].annotations[2].infons

    d.passages[0].annotations[0].infons['CUI'] = 'xxx'
    d.passages[0].annotations[2].infons['CUI'] = 'xxx'
    _extend(d, 'negation')
    assert 'negation' not in d.passages[0].annotations[2].infons
