import logging
from typing import List, Dict, Tuple, Match

import bioc
import yaml
import re
from negbio.pipeline2.pipeline import Pipe
from negbio.neg import semgraph, propagator, utils
from negbio import ngrex


UNCERTAINTY = "uncertainty"
NEGATION = "negation"
REPORTS = "Reports"


def load_regex_yml(filename) -> List[Dict]:
    """
    Read a pattern file in the yaml format

    Args:
        filename(str): file name

    Returns:
        list: a list of dict NgexPattern
    """
    with open(filename) as fp:
        patterns = yaml.load(fp, yaml.FullLoader)

    for p in patterns:
        p['patternobj'] = re.compile(p['pattern'], re.I)
    return patterns


class Detector2:
    def __init__(self, pre_negation_uncertainty_path,
                 negation_path, post_negation_uncertainty_path,
                 negation_regex_path, uncertainty_regex_path):
        npatterns = ngrex.load_yml(negation_path)
        self.neg_patterns = [p['patternobj'] for p in npatterns]

        upatterns = ngrex.load_yml(post_negation_uncertainty_path)
        self.uncertain_patterns = [p['patternobj'] for p in upatterns]

        pupatterns = ngrex.load_yml(pre_negation_uncertainty_path)
        self.preneg_uncertain_patterns = [p['patternobj'] for p in pupatterns]

        n_regex_patterns = load_regex_yml(negation_regex_path)
        self.neg_regex_patterns = [p['patternobj'] for p in n_regex_patterns]

        u_regex_patterns = load_regex_yml(uncertainty_regex_path)
        self.uncertain_regex_patterns = [p['patternobj'] for p in u_regex_patterns]

        self.total_patterns = {p['patternobj']: p for p in
                               npatterns + upatterns + pupatterns
                               + n_regex_patterns + u_regex_patterns}

    def regex_detect(self, sentence, locs):
        """Detect regular expression rules in report sentences.

        Args:
            sentence(BioCSentence): a sentence with universal dependencies
            locs(list): a list of (begin, end)

        Return:
            (str, MatcherObj, (begin, end)): negation or uncertainty,
            matcher, matched annotation
        """
        for loc in locs:
            neg_m = self.match_neg_regex(sentence, loc)
            if neg_m:
                yield NEGATION, neg_m, loc
            else:
                uncertain_m = self.match_uncertain_regex(sentence, loc)
                if uncertain_m:
                    yield UNCERTAINTY, uncertain_m, loc

    def detect(self, sentence, locs):
        """Detect rules in report sentences.

        Args:
            sentence(BioCSentence): a sentence with universal dependencies
            locs(list): a list of (begin, end)

        Return:
            (str, MatcherObj, (begin, end)): negation or uncertainty,
            matcher, matched annotation
        """
        # regular expression
        matched_locs = []
        for loc in locs:
            neg_m = self.match_neg_regex(sentence, loc)
            if neg_m:
                yield NEGATION, neg_m, loc
                matched_locs.append(loc)
            else:
                uncertain_m = self.match_uncertain_regex(sentence, loc)
                if uncertain_m:
                    yield UNCERTAINTY, uncertain_m, loc
                    matched_locs.append(loc)

        for l in matched_locs:
            locs.remove(l)

        try:
            g = semgraph.load(sentence)
            propagator.propagate(g)
        except Exception:
            logging.exception('Cannot parse dependency graph [offset=%s]', sentence.offset)
            raise
        else:
            for loc in locs:
                for node in find_nodes(g, loc[0], loc[1]):
                    # Match pre-negation uncertainty rules first.
                    preneg_m = self.match_prenegation_uncertainty(g, node)
                    if preneg_m:
                        yield UNCERTAINTY, preneg_m, loc
                    else:
                        # Then match negation rules.
                        neg_m = self.match_neg(g, node)
                        if neg_m:
                            yield NEGATION, neg_m, loc
                        else:
                            # Finally match post-negation uncertainty rules.
                            postneg_m = self.match_uncertainty(g, node)
                            if postneg_m:
                                yield UNCERTAINTY, postneg_m, loc

    def graph_detect(self, sentence, locs):
        """Detect rules in report sentences.

        Args:
            sentence(BioCSentence): a sentence with universal dependencies
            locs(list): a list of (begin, end)

        Return:
            (str, MatcherObj, (begin, end)): negation or uncertainty,
            matcher, matched annotation
        """
        try:
            g = semgraph.load(sentence)
            propagator.propagate(g)
        except Exception:
            logging.exception('Cannot parse dependency graph [offset=%s]', sentence.offset)
            raise
        else:
            for loc in locs:
                for node in find_nodes(g, loc[0], loc[1]):
                    # Match pre-negation uncertainty rules first.
                    preneg_m = self.match_prenegation_uncertainty(g, node)
                    if preneg_m:
                        yield UNCERTAINTY, preneg_m, loc
                    else:
                        # Then match negation rules.
                        neg_m = self.match_neg(g, node)
                        if neg_m:
                            yield NEGATION, neg_m, loc
                        else:
                            # Finally match post-negation uncertainty rules.
                            postneg_m = self.match_uncertainty(g, node)
                            if postneg_m:
                                yield UNCERTAINTY, postneg_m, loc

    def match_uncertainty(self, graph, node):
        for pattern in self.uncertain_patterns:
            for m in pattern.finditer(graph):
                n0 = m.group(0)
                if n0 == node:
                    return m

    def match_prenegation_uncertainty(self, graph, node):
        for pattern in self.preneg_uncertain_patterns:
            for m in pattern.finditer(graph):
                n0 = m.group(0)
                if n0 == node:
                    return m

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

    def match_neg_regex(self, sentence: bioc.BioCSentence, loc: Tuple[int, int]):
        text = get_text(sentence, loc)
        for pattern in self.neg_regex_patterns:
            m = pattern.search(text)
            if m:
                return m

    def match_uncertain_regex(self, sentence, loc):
        text = get_text(sentence, loc)
        for pattern in self.uncertain_regex_patterns:
            m = pattern.search(text)
            if m:
                return m


def get_text(sentence: bioc.BioCSentence, loc: Tuple[int, int]):
    text = sentence.text
    start = loc[0] - sentence.offset
    end = loc[1] - sentence.offset
    text = text[:start] + '$X$' + text[end:]
    text = re.sub(' {2,}', ' ', text)
    return text


def neg_mesh(annotations):
    """
    Detect negative MeSH
    """
    for ann in annotations:
        if ann.infons.get('CUI', None) == 'C0332125':
            ann.infons[NEGATION] = 'True'


def uncertain_mesh(annotations):
    """
    Detect uncertain MeSH
    """
    for ann in annotations:
        if ann.infons.get('CUI', None) == 'C0332148':
            ann.infons[UNCERTAINTY] = 'True'


def find_nodes(graph, begin, end):
    for node in graph.nodes():
        if utils.intersect((begin, end), (graph.node[node]['start'], graph.node[node]['end'])):
            yield node


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


class NegBioNegDetector2(Pipe):
    def __init__(self, detector: Detector2):
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
                    # for name, matcher, loc in self.detector.regex_detect(sentence, sublocs):
                    #     _mark_anns(passage.annotations, loc[0], loc[1], name,
                    #                self.detector.total_patterns[matcher.pattern])
                    # for name, matcher, loc in self.detector.graph_detect(sentence, sublocs):
                    #     _mark_anns(passage.annotations, loc[0], loc[1], name,
                    #                self.detector.total_patterns[matcher.pattern])
                    for name, matcher, loc in self.detector.detect(sentence, sublocs):
                        if isinstance(matcher, Match):
                            _mark_anns(passage.annotations, loc[0], loc[1], name,
                                       self.detector.total_patterns[matcher.re])
                        else:
                            _mark_anns(passage.annotations, loc[0], loc[1], name,
                                       self.detector.total_patterns[matcher.pattern])

            # _extend(document, Detector.NEGATION)
            # _extend(document, Detector.UNCERTAINTY)
        except:
            logging.exception("Cannot process %s", doc.id)
        return doc
