import copy
from pathlib import Path

import bioc

import negbio
from negbio.pipeline2.dner_regex import RegExExtractor
from tests.negbio.utils import get_example_dir


__project_dir = Path(negbio.__file__).parent.parent


def test_chexpert_extractor():
    phrases_dir = __project_dir / 'patterns'
    extractor = RegExExtractor(phrases_dir / 'chexpert_phrases.yml', 'CheXpert labeler')

    dir = get_example_dir()
    with open(dir / '1.chexpert.xml') as fp:
        c = bioc.load(fp)

    actual_documents = c.documents
    expected_documents = []
    for doc in actual_documents:
        doc = copy.deepcopy(doc)
        for p in doc.passages:
            del p.annotations[:]
        expected_documents.append(doc)

    for expected_doc, actual_doc in zip(expected_documents, actual_documents):
        extractor.__call__(expected_doc)
        expected_anns = sorted(list(bioc.annotations(expected_doc, bioc.PASSAGE)),
                               key=lambda a: a.total_span.offset)
        actual_anns = sorted(list(bioc.annotations(actual_doc, bioc.PASSAGE)),
                             key=lambda a: a.total_span.offset)

        assert len(expected_anns) == len(actual_anns), \
            '{} vs {}'.format(len(expected_anns), len(actual_anns))
        for expected_ann, actual_ann in zip(expected_anns, actual_anns):
            assert expected_ann.total_span == actual_ann.total_span
            for k in ['observation', 'annotator']:
                assert expected_ann.infons[k] == actual_ann.infons[k]


if __name__ == '__main__':
    test_chexpert_extractor()
