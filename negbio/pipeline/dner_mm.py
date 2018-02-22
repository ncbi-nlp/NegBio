"""
Detect UMLS concept

Usage:
    dner_mm [--cuis=FILE] --metamap=BINARY --out=DIRECTORY SOURCE ...

Options:
    --metamap=BINARY    The MetaMap binary
    --cuis=FILE         CUI list [default: None]
"""
from __future__ import print_function

import itertools
import logging
import re
import sys

import bioc
import docopt

import pymetamap
from negbio.pipeline import scan
import re
import collections


def remove_newline(s):
    return re.sub(r'[\n\r]', ' ', s)


def adapt_concept_index(index):
    m = re.match(r"'.*?'", index)
    if m:
        return index[1:-1]
    else:
        return index


def run_metamap_col(collection, mm, cuis=None):
    """
    Get CUIs from metamap.

    Args:
        collection(BioCCollection):
        mm(MetaMap): MetaMap instance

    Returns:
        BioCCollection
    """
    try:
        annIndex = itertools.count()
        sentence_map = collections.OrderedDict()
        for document in collection.documents:
            for passage in document.passages:
                for sentence in passage.sentences:
                    sentence_map['{}-{}'.format(document.id, sentence.offset)] = (passage, sentence)

        sents = []
        ids = []
        for k in sentence_map:
            ids.append(k)
            sents.append(remove_newline(sentence_map[k][1].text))

        concepts, error = mm.extract_concepts(sents, ids)
        if error is None:
            for concept in concepts:
                concept_index = adapt_concept_index(concept.index)
                try:
                    if cuis is not None and concept.cui not in cuis:
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
        logging.exception("Cannot process %s", collection.source)
    return collection


def run_metamap(document, mm, cuis=None):
    """
    Get CUIs from metamap.

    Args:
        document(BioCDocument):
        mm(MetaMap): MetaMap instance

    Returns:
        BioCDocument
    """
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

        concepts, error = mm.extract_concepts(sents, ids)
        print('Done')
        if error is None:
            for concept in concepts:
                # print(concept)
                concept_index = adapt_concept_index(concept.index)
                try:
                    if cuis is not None and concept.cui not in cuis:
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


def read_cuis(pathname):
    cuis = set()
    with open(pathname) as fp:
        for line in fp:
            line = line.strip()
            if line:
                cuis.add(line)
    return cuis


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    mm = pymetamap.MetaMap.get_instance(argv['--metamap'])

    if argv['--cuis'] == 'None':
        cuis = None
    else:
        cuis = read_cuis(argv['--cuis'])

    scan.scan_collection(source=argv['SOURCE'], directory=argv['--out'], suffix='.mm.xml',
                         fn=run_metamap_col, non_sequences=[mm, cuis])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    main(sys.argv[1:])
