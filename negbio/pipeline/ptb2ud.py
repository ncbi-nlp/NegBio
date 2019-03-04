import logging

import StanfordDependencies
import bioc
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.mapping import tagset_mapping


class Lemmatizer(object):
    def __init__(self):
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.mapping = tagset_mapping('en-ptb', 'universal')

    def lemmatize(self, word, pos=None):
        """
        Determines the lemma for a given word

        Args:
            word(str): word
            pos(str): part-of-speech

        Returns:
            str: lemma
        """
        if pos:
            return self.wordnet_lemmatizer.lemmatize(word=word, pos=pos)
        else:
            return self.wordnet_lemmatizer.lemmatize(word=word)

    def map_tag(self, tag):
        if tag in self.mapping:
            tag = self.mapping[tag]
            if tag == 'NOUN':
                return wordnet.NOUN
            elif tag == 'VERB':
                return wordnet.VERB
            elif tag == 'ADJ':
                return wordnet.ADJ
            elif tag == 'ADV':
                return wordnet.ADV
            elif tag == 'ADJ_SAT':
                return wordnet.ADJ_SAT
        return None


class Ptb2DepConverter(object):
    """
    Convert ptb trees to universal dependencies
    """

    basic = 'basic'
    collapsed = 'collapsed'
    CCprocessed = 'CCprocessed'
    collapsedTree = 'collapsedTree'

    def __init__(self, lemmatizer, representation='CCprocessed', universal=False):
        """
        Args:
            representation(str): Currently supported representations are
                'basic', 'collapsed', 'CCprocessed', and 'collapsedTree'
            universal(bool): if True, use universal dependencies if they're available
        """
        try:
            import jpype
            self._backend = 'jpype'
        except ImportError:
            self._backend = 'subprocess'
        self.lemmatizer = lemmatizer
        self.__sd = StanfordDependencies.get_instance(backend=self._backend)
        self.representation = representation
        self.universal = universal

    def convert(self, parse_tree):
        """
        Convert ptb trees in a BioC sentence

        Args:
            parse_tree(str): parse tree in PTB format

        Examples:
            (ROOT (NP (JJ hello) (NN world) (. !)))
        """
        if self._backend == 'jpype':
            dependency_graph = self.__sd.convert_tree(parse_tree,
                                                      representation=self.representation,
                                                      universal=self.universal,
                                                      add_lemmas=True)
        else:
            dependency_graph = self.__sd.convert_tree(parse_tree,
                                                      representation=self.representation,
                                                      universal=self.universal)
        return dependency_graph


class NegBioPtb2DepConverter(Ptb2DepConverter):
    def __init__(self, lemmatizer, representation='CCprocessed', universal=False):
        """
        Args:
            lemmatizer (Lemmatizer)
        """
        super(NegBioPtb2DepConverter, self).__init__(
            lemmatizer, representation, universal)

    def convert_doc(self, document):
        for passage in document.passages:
            for sentence in passage.sentences:
                # check for empty infons, don't process if empty
                # this sometimes happens with poorly tokenized sentences
                if not sentence.infons:
                    continue
                elif not sentence.infons['parse tree']:
                    continue

                try:
                    dependency_graph = self.convert(
                        sentence.infons['parse tree'])
                    anns, rels = convert_dg(dependency_graph, sentence.text,
                                            sentence.offset,
                                            has_lemmas=self._backend == 'jpype')
                    sentence.annotations = anns
                    sentence.relations = rels
                except KeyboardInterrupt:
                    raise
                except:
                    logging.exception(
                        "Cannot process sentence %d in %s", sentence.offset, document.id)

                if self._backend != 'jpype':
                    for ann in sentence.annotations:
                        text = ann.text
                        pos = ann.infons['tag']
                        pos = self.lemmatizer.map_tag(pos)
                        lemma = self.lemmatizer.lemmatize(word=text, pos=pos)
                        ann.infons['lemma'] = lemma.lower()
        return document


def adapt_value(value):
    """
    Adapt string in PTB
    """
    value = value.replace("-LRB-", "(")
    value = value.replace("-RRB-", ")")
    value = value.replace("-LSB-", "[")
    value = value.replace("-RSB-", "]")
    value = value.replace("-LCB-", "{")
    value = value.replace("-RCB-", "}")
    value = value.replace("-lrb-", "(")
    value = value.replace("-rrb-", ")")
    value = value.replace("-lsb-", "[")
    value = value.replace("-rsb-", "]")
    value = value.replace("``", "\"")
    value = value.replace("''", "\"")
    value = value.replace("`", "'")
    return value


def convert_dg(dependency_graph, text, offset, ann_index=0, rel_index=0, has_lemmas=True):
    """
    Convert dependency graph to annotations and relations
    """
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
                logging.debug('Cannot convert parse tree to dependency graph at %d\n%d\n%s',
                              start, offset, str(dependency_graph))
                return

        ann = bioc.BioCAnnotation()
        ann.id = 'T{}'.format(ann_index)
        ann.text = node_form
        ann.infons['tag'] = node.pos
        if has_lemmas:
            ann.infons['lemma'] = node.lemma.lower()

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
        relation.add_node(bioc.BioCNode('T{}'.format(
            annotation_id_map[node.index]), 'dependant'))
        relation.add_node(bioc.BioCNode('T{}'.format(
            annotation_id_map[node.head]), 'governor'))
        relations.append(relation)
        rel_index += 1

    return annotations, relations
