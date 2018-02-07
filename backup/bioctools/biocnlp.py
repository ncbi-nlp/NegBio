import logging

import bioc
from pynih import nlp as nlp
from pynih.nlp.ptb2dep import adapt_value


def ssplit_d(splitter, document):
    """

    Args:
        splitter(Splitter):
        document(BioCDocument):

    Returns:

    """
    for passage in document.passages:
        for text, offset in splitter.split(passage.text):
            sentence = bioc.BioCSentence()
            sentence.offset = offset + passage.offset
            sentence.text = text
            passage.add_sentence(sentence)
        passage.text = None


def ssplit_f(splitter, src, dst):
    """
    Split a BioC file.

    Args:
        splitter(Splitter):
        src(str): source file name in BioC format
        dst(str): target file name in BioC format
    """
    logging.debug('Process file: %s', src)

    with bioc.iterparse(src) as parser:
        with bioc.iterwrite(dst, parser.get_collection_info()) as writer:
            for document in parser:
                ssplit_d(splitter, document)
                writer.writedocument(document)


def capitalize_f(src, dst):
    logger = logging.getLogger(__name__)

    with bioc.iterparse(src) as parser:
        with bioc.iterwrite(dst, parser.get_collection_info()) as writer:
            for document in parser:
                for passage in document.passages:
                    for sentence in passage.sentences:
                        if sentence.text:
                            sentence.text = nlp.capitalize(sentence.text)
                            logger.debug('{}: {}'.format(sentence.offset, sentence.text))
                writer.writedocument(document)


def parses(parser, sentence):
    """
    Parse one sentence in BioC format

    Args:
        parser(Bllip)
        sentence(BioCSentence): one sentence in BioC format
    """
    try:
        text = sentence.text
        tree = parser.parse(text)
        sentence.infons['parse tree'] = tree
    except:
        raise ValueError('Cannot parse sentence: {}'.format(sentence.offset))


def parsef(parser, src, dst, sentence_filter=None):
    """
    Parse sentences in BioC format when sentence_filter returns true

    Args:
        parser(Bllip)
        src(str): source file name in BioC format
        dst(str): target file name in BioC format
        sentence_filter: only parse the sentence when sentence_filter returns true
    """

    def true(*_):
        return True

    if sentence_filter is None:
        sentence_filter = true

    logger = logging.getLogger(__name__)

    with bioc.iterparse(src) as biocparser:
        collection = biocparser.get_collection_info()
        collection.infons['tool'] = 'Bllip'
        collection.infons['process'] = 'parse'
        with bioc.iterwrite(dst, collection) as writer:
            for document in biocparser:
                logger.debug('Parse document: %s' % document.id)
                for passage in document.passages:
                    for sentence in filter(sentence_filter, passage.sentences):
                        try:
                            parses(sentence, parser)
                        except:
                            logger.exception(
                                'Some errors for parsing sentence: {}'.format(sentence.offset))
                writer.writedocument(document)


def lemmatize_s(lemmatizer, sentence):
    for ann in sentence.annotations:
        text = ann.text
        pos = ann.infons['tag']
        pos = lemmatizer.map_tag(pos)
        lemma = lemmatizer.lemmatize(word=text, pos=pos)
        ann.infons['lemma'] = lemma.lower()


def lemmatize_c(lemmatizer, collection):
    for doc in collection.documents:
        lemmatize_d(lemmatizer, doc)


def lemmatize_d(lemmatizer, document):
    for passage in document.passages:
        for sentence in passage.sentences:
            lemmatize_s(lemmatizer, sentence)


def lemmatize_f(lemmatizer, src, dst):
    """
    Determines the lemma for a given word

    Args:
        src(str): source file name in BioC format
        dst(str): target file name in BioC format
    """
    logger = logging.getLogger(__name__)
    logger.info("Processing {}".format(src))

    with bioc.iterparse(src) as parser:
        collection = parser.get_collection_info()
        with bioc.iterwrite(dst, collection) as writer:
            for document in parser:
                lemmatize_d(lemmatizer, document)
                writer.writedocument(document)


def convert_s(ptb2dep, sentence):
    """
    Convert ptb trees in a BioC sentence
    """
    if 'parse tree' not in sentence.infons:
        return
    dependency_graph = ptb2dep.convert(sentence.infons['parse tree'])
    anns, rels = convert_dg(dependency_graph, sentence.text, sentence.offset)
    sentence.annotations = anns
    sentence.relations = rels


def convert_c(ptb2dep, collection):
    """
    Convert ptb trees in BioC collection
    """
    logger = logging.getLogger(__name__)
    for document in collection.documents:
        logger.debug('Processing document: %s', document.id)
        for passage in document.passages:
            for sentence in passage.sentences:
                try:
                    convert_s(ptb2dep, sentence)
                except:
                    logger.exception("Cannot process sentence %d in %s",
                                     sentence.offset, document.id)


def convert_f(ptb2dep, src, dst):
    """
    Convert from BioC src file to BioC dst file

    Args:
        ptb2dep(Ptb2Dep):
        src(str): source file name in BioC format
        dst(str): target file name in BioC format
    """
    logger = logging.getLogger(__name__)
    logger.info("Processing %s", src)

    try:
        with bioc.iterparse(src) as parser:
            with bioc.iterwrite(dst, parser.get_collection_info()) as writer:
                for document in parser:
                    logger.debug('Processing document: %s', document.id)
                    for passage in document.passages:
                        for sentence in passage.sentences:
                            try:
                                convert_s(ptb2dep, sentence)
                            except:
                                logger.exception("Cannot process sentence %d in %s",
                                                 sentence.offset, document.id)
                    writer.writedocument(document)
    except Exception:
        logger.exception("Cannot process %s", src)
        return


def convert_dg(dependency_graph, text, offset, ann_index=0, rel_index=0):
    """
    Convert dependency graph to annotations and relations
    """
    logger = logging.getLogger(__name__)
    annotations = []
    relations = []
    annotation_id_map = {}
    start = 0
    for node in dependency_graph:
        if node.index in annotation_id_map:
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

        ann = bioc.BioCAnnotation()
        ann.id = 'T{}'.format(ann_index)
        ann.text = node_form
        ann.infons['tag'] = node.pos

        start = index

        ann.add_location(bioc.BioCLocation(start + offset, len(node_form)))
        annotations.append(ann)
        annotation_id_map[node.index] = ann_index
        ann_index += 1
        start += len(node_form)

    for node in dependency_graph:
        if node.head == 0:
            ann = annotations[annotation_id_map[node.index]]
            ann.infons['ROOT'] = True
            continue
        relation = bioc.BioCRelation()
        relation.id = 'R{}'.format(rel_index)
        relation.infons['dependency'] = node.deprel
        if node.extra:
            relation.infons['extra'] = node.extra
        relation.add_node(bioc.BioCNode('T{}'.format(annotation_id_map[node.index]), 'dependant'))
        relation.add_node(bioc.BioCNode('T{}'.format(annotation_id_map[node.head]), 'governor'))
        relations.append(relation)
        rel_index += 1

    return annotations, relations
