from __future__ import print_function

import logging

from negbio.neg import utils, semgraph, propagator
from negbio import ngrex

NEGATION = 'negation'
UNCERTAINTY = 'uncertainty'


class Detector(object):

    NEGATION = 'negation'
    UNCERTAINTY = 'uncertainty'

    def __init__(self,
                 neg_pattern_file,
                 uncertainty_pattern_file,
                 sentence_rule=False):
        self.sentence_rule = sentence_rule
        self.neg_patterns = ngrex.load(neg_pattern_file)
        self.uncertain_patterns = ngrex.load(uncertainty_pattern_file)

    def detect(self, sentence, locs):
        """
        Args:
            sentence(BioCSentence): a sentence with universal dependencies
            locs(list): a list of (begin, end)
        Yields:
            (str, MatcherObj, (begin, end)): negation or uncertainty, matcher, matched annotation
        """
        try:
            g = semgraph.load(sentence)
            propagator.propagate(g)
        except:
            logging.exception('Cannot parse dependency graph [offset={}]'.format(sentence.offset))
            raise
        else:
            if self.sentence_rule and is_neg_graph1(g):
                for loc in locs:
                    yield NEGATION, None, loc
                return
            for loc in locs:
                if self.sentence_rule and is_neg_graph2(g, loc[0], loc[1]):
                    yield NEGATION, None, loc
                for node in find_nodes(g, loc[0], loc[1]):
                    m = self.match_neg(g, node)
                    if m:
                        yield NEGATION, m, loc
                    m = self.match_uncertainty(g, node)
                    if m:
                        yield UNCERTAINTY, m, loc

    def match_neg(self, graph, node):
        """
        Returns a matcher
        """
        for pattern in self.neg_patterns:
            for m in pattern.finditer(graph):
                n0 = m.group(0)
                if n0 == node:
                    try:
                        key = m.get('key')
                        if semgraph.has_out_edge(graph, key, ['neg']):
                            continue
                    except:
                        pass
                    if semgraph.has_out(graph, n0, ['new'], ['amod']):
                        continue
                    return m
        return None

    def match_uncertainty(self, graph, node):
        for pattern in self.uncertain_patterns:
            for m in pattern.finditer(graph):
                n0 = m.group(0)
                if n0 == node:
                    return m

        # parsing error
        # suggestive of XXX
        p = ngrex.compile('{} <{dependency:/nmod:of/} {lemma:/suggestive/}')
        for m in p.finditer(graph):
            n0 = m.group(0)
            if n0 == node:
                if semgraph.has_out_node(graph, m.group(1), ['most']):
                    return None
                elif semgraph.has_out(graph, n0, ['new', 'develop'], ['amod']):
                    continue
                else:
                    return m
        return None


def find_nodes(graph, begin, end):
    for node in graph.nodes():
        if utils.intersect((begin, end), (graph.node[node]['start'], graph.node[node]['end'])):
            yield node


def is_neg_graph1(graph):
    # no XXX
    # resolution of XXX
    if 'T0' in graph.node and graph.node['T0']['lemma'] in ['no', 'resolution', 'resolved']:
        # no verb
        has_verb = utils.contains(lambda x: graph.node[x]['tag'][0] == 'V', graph.nodes())
        if not has_verb:
            return True
    return False


def is_neg_graph2(graph, begin, end):
    """
    Return True if the sentence is like "without [begin, end]"

    """

    # without n [, n]
    state = 0
    # sort nodes
    for node in sorted(graph.nodes(), key=lambda n: graph.node[n]['start']):
        if graph.node[node]['end'] > end:
            break

        if state == 0:
            if graph.node[node]['lemma'] in (
                    'without', 'no', 'resolve', 'resolution', 'rosolution'):
                state = 1
        elif state == 1:
            if graph.node[node]['tag'].startswith('N'):
                state = 1
                if utils.intersect((begin, end), (graph.node[node]['start'], graph.node[node]['end'])):
                    return True
            elif graph.node[node]['tag'] in ('JJ', 'CC', ',', 'VBN'):
                state = 1
            else:
                return False
    return False


def is_neg(annotation):
    return NEGATION in annotation.infons and annotation.infons[NEGATION] == 'True'


def is_uncertain(annotation):
    return UNCERTAINTY in annotation.infons and annotation.infons[UNCERTAINTY] == 'True'
