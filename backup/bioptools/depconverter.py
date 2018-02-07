import itertools
import logging

import biop
from biop import biopitertools
from pynih.nlp.ptb2dep import adapt_value


def convert_f(ptb2dep, src, dst):
    """
    Convert ptb tree to universal dependencies from BioP src file to BioP dst file

    Args:
        ptb2dep(Ptb2Dep):
        src(str): source file name in BioP format
        dst(str): target file name in BioP format
    """
    logging.info("Processing %s", src)

    with open(src) as fp:
        document = biop.load(fp)

    for sentence in biopitertools.sentences(document):
        try:
            if 'parse tree' not in sentence.attributes:
                continue
            dependency_graph = ptb2dep.convert(sentence.attributes['parse tree'])
            convert_dg(document, dependency_graph, sentence.total_text, sentence.begin)
        except:
            logging.exception("Cannot process sentence %d in %s",
                              sentence.begin, document.id)

    with open(dst, 'w') as fp:
        biop.dump(document, fp)


def convert_dg(document, dependency_graph, text, offset):
    """
    Convert dependency graph to annotations and relations
    """
    ann_index = itertools.count(document.max_id + 1)

    # import pdb;pdb.set_trace()

    logger = logging.getLogger(__name__)
    nodeid2annid = {}

    start = 0
    for node in dependency_graph:
        if node.index in nodeid2annid:
            continue
        node_form = node.form
        index = text.find(node_form, start)
        if index == -1:
            node_form = adapt_value(node.form)
            index = text.find(node_form, start)
            if index == -1:
                logger.debug('Cannot convert parse tree to dependency graph at %d\n%d\n%s',
                             start, offset, str(dependency_graph))
                return

        ann = biop.PAnnotation()
        ann.id = next(ann_index)
        ann.type = biop.TOKEN
        ann.attributes['tag'] = node.pos

        start = index
        ann.add_location(biop.PLocation(start + offset,
                                        start + offset + len(node_form),
                                        node_form))
        nodeid2annid[node.index] = ann.id
        document.add_annotation(ann)
        start += len(node_form)

    for node in dependency_graph:
        if node.head == 0:
            id = nodeid2annid[node.index]
            ann = biopitertools.ann_id(document, id)
            ann.attributes['ROOT'] = True
            continue
        relation = biop.PRelation()
        relation.id = next(ann_index)
        relation.type = 'UD'
        relation.attributes['dependency'] = node.deprel
        if node.extra:
            relation.attributes['extra'] = node.extra
        relation.nodes.append(biop.PNode(nodeid2annid[node.index], 'dependant'))
        relation.nodes.append(biop.PNode(nodeid2annid[node.head], 'governor'))
        document.relations.append(relation)
