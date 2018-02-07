from __future__ import print_function

import logging
import re

import bioc
import biop
from biop import biopitertools
from pynih.negbio2 import Detector


def neg_mesh(annotations):
    """
    Detect negative MeSH
    """
    for ann in annotations:
        if ann.attributes.get('CUI', None) == 'C0332125':
            ann.attributes[Detector.NEGATION] = 'True'


def uncertain_mesh(annotations):
    """
    Detect uncertain MeSH
    """
    for ann in annotations:
        if ann.attributes.get('CUI', None) == 'C0332148':
            ann.attributes[Detector.UNCERTAINTY] = 'True'


def is_neg_regex(text):
    pattern1 = re.compile(r'^(findings|impression): no ', re.I)
    if pattern1.search(text):
        return True
    return False


def neg_disease(uddocument, mmdocument, detector=Detector()):
    """
    Args:
        uddocument(PDocument): a UD document
        mmdocument(PDocument): a MM document
        detector(Detector): detector. Define customized patterns in the detector
    """
    logger = logging.getLogger(__name__)

    def _mark_anns(document, begin, end, type):
        """Mark all annotations in [begin:end] as type"""
        for iv in document.annotation_tree.search(begin, end + 1, strict=True):
            print('x', type)
            mm_ann = iv.data
            mm_ann.attributes[type] = 'True'

    def _extend(annotations, type):
        def _is_type(annotation):
            return annotation.attributes.get(type, None) == 'True'

        neg_anns = [ann for ann in annotations if _is_type(ann)]
        for ann in annotations:
            if _is_type(ann):
                continue
            for nann in neg_anns:
                if ann in nann:
                    ann.attributes[type] = 'True'
                    break
                if nann in ann \
                        and 'CUI' in ann \
                        and 'CUI' in nann \
                        and ann.attributes['CUI'] == nann.infons['CUI']:
                    ann.attributes[type] = 'True'
                    break

    try:
        neg_mesh(mmdocument.annotations)
        uncertain_mesh(mmdocument.annotations)

        for sen in biopitertools.sentences(uddocument):
            udsendocument = biop.sub(uddocument, sen.begin, sen.end)
            mmsendocument = biop.sub(mmdocument, sen.begin, sen.end)

            if is_neg_regex(sen.total_text):
                _mark_anns(mmsendocument, sen.begin, sen.end, Detector.NEGATION)
                continue

            locs = [(ann.begin, ann.end) for ann in mmsendocument.annotations]

            biocsen = bioc.BioCSentence()
            biocsen.offset = sen.begin
            biocsen.text = sen.total_text
            for ann in biopitertools.tokens(udsendocument):
                biocann = bioc.BioCAnnotation()
                biocann.id = ann.id
                biocann.infons['lemma'] = ann.attributes['lemma']
                biocann.infons['tag'] = ann.attributes['tag']
                biocann.text = ann.total_text
                biocann.add_location(bioc.BioCLocation(ann.begin, ann.end - ann.begin))
                biocsen.add_annotation(biocann)
            for rel in udsendocument.relations:
                biocrel = bioc.BioCRelation()
                biocrel.id = rel.id
                biocrel.infons['dependency'] = rel.attributes['dependency']
                for node in rel.nodes:
                    biocrel.nodes.append(bioc.BioCNode(node.refid, node.role))
                biocsen.add_relation(biocrel)

            # print(biocsen)

            for name, matcher, loc in detector.detect(biocsen, locs):
                logging.debug('Find: %s, %s, %s', name, matcher.pattern, loc)
                _mark_anns(mmsendocument, loc[0], loc[1], name)

        _extend(mmdocument.annotations, Detector.NEGATION)
        _extend(mmdocument.annotations, Detector.UNCERTAINTY)
    except:
        logger.exception("Cannot process %s", mmdocument.id)
