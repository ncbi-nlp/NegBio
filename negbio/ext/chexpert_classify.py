"""Define mention classifier class.

Author: stanfordmlgroup
Modified by: Yifan Peng
"""
import logging

from negbio import ngrex
from negbio.neg import semgraph, propagator, neg_detector


UNCERTAINTY = "uncertainty"
NEGATION = "negation"
REPORTS = "Reports"


class CheXpertDetector(neg_detector.Detector):
    """Child class of NegBio Detector class.

    Overrides parent methods __init__, detect, and match_uncertainty.
    """

    def __init__(self, pre_negation_uncertainty_path,
                 negation_path, post_negation_uncertainty_path):
        super(CheXpertDetector, self).__init__(negation_path, post_negation_uncertainty_path)
        pupatterns = ngrex.load_yml(pre_negation_uncertainty_path)
        self.preneg_uncertain_patterns = [p['patternobj'] for p in pupatterns]
        self.total_patterns.update({p['patternobj']: p for p in pupatterns})

    def detect(self, sentence, locs):
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
                for node in neg_detector.find_nodes(g, loc[0], loc[1]):
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

