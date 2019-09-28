import collections
import itertools
import logging
import re

import bioc

from pipeline2.pipeline import Pipe


def remove_newline(s):
    return re.sub(r'[\n\r]', ' ', s)


def adapt_concept_index(index):
    m = re.match(r"'.*?'", index)
    if m:
        return index[1:-1]
    m = re.match(r"'.*", index)
    if m:
        return index[1:]
    return index


class MetaMapExtractor(Pipe):
    """
    Get CUIs from metamap.
    """
    def __init__(self, mm, cuis=None):
        """
        Args:
            document(BioCDocument):
            mm(MetaMap): MetaMap instance
        """
        self.mm = mm
        self.cuis = cuis

    def __call__(self, document, *args, **kwargs):
        try:
            annIndex = itertools.count()
            sentence_map = collections.OrderedDict()
            for passage in document.passages:
                for sentence in passage.sentences:
                    sentence_map[str(sentence.offset)] = (passage, sentence)

            sents = []
            ids = []
            for k in sentence_map:
                ids.append(k)
                sents.append(remove_newline(sentence_map[k][1].text))

            concepts, error = self.mm.extract_concepts(sents, ids)
            if error is None:
                for concept in concepts:
                    concept_index = adapt_concept_index(concept.index)
                    try:
                        if self.cuis is not None and concept.cui not in self.cuis:
                            continue
                        m = re.match(r'(\d+)/(\d+)', concept.pos_info)
                        if m:
                            passage = sentence_map[concept_index][0]
                            sentence = sentence_map[concept_index][1]
                            start = int(m.group(1)) - 1
                            length = int(m.group(2))
                            ann = bioc.BioCAnnotation()
                            ann.id = str(next(annIndex))
                            ann.infons['CUI'] = concept.cui
                            ann.infons['semtype'] = concept.semtypes[1:-1]
                            ann.infons['term'] = concept.preferred_name
                            ann.infons['annotator'] = 'MetaMap'
                            ann.add_location(bioc.BioCLocation(sentence.offset + start, length))
                            ann.text = sentence.text[start:start+length]
                            passage.annotations.append(ann)
                    except:
                        logging.exception('')
        except:
            logging.exception("Cannot process %s", document.id)
        return document
