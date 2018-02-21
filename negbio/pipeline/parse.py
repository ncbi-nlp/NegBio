"""
Parse sentences

Usage:
    parse [options] --out=DIRECTORY SOURCE ...

Options:
    --model=MODEL_DIR               Bllip parser model directory
"""
from __future__ import print_function, absolute_import

import logging
import os
import sys
import tempfile

import docopt
from bllipparser import ModelFetcher
from bllipparser import RerankingParser

from negbio.pipeline import scan


class Bllip:
    def __init__(self, model_dir=None):
        if model_dir is None:
            logging.debug("downloading GENIA+PubMed model if necessary ...")
            model_dir = ModelFetcher.download_and_install_model(
                'GENIA+PubMed', os.path.join(tempfile.gettempdir(), 'models'))
        self.model_dir = os.path.expanduser(model_dir)

        logging.debug('loading model %s ...' % self.model_dir)
        self.rrp = RerankingParser.from_unified_model_dir(self.model_dir)

    def parse(self, s):
        """Parse the sentence text using Reranking parser.

        Args:
            s(str): one sentence

        Returns:
            ScoredParse: parse tree, ScoredParse object in RerankingParser; None if failed
        """
        if not s:
            raise ValueError('Cannot parse empty sentence: {}'.format(s))
        try:
            nbest = self.rrp.parse(str(s))
            return nbest[0].ptb_parse
        except:
            raise ValueError('Cannot parse sentence: %s' % s)


def parse(document, parser):
    """
    Parse sentences in BioC format when sentence_filter returns true

    Args:
        parser(Bllip)
        document(BioCDocument): one document
    """
    for passage in document.passages:
        for sentence in passage.sentences:
            try:
                text = sentence.text
                tree = parser.parse(text)
                sentence.infons['parse tree'] = str(tree)
            except:
                raise ValueError('Cannot parse sentence: {}'.format(sentence.offset))
    return document


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    parser = Bllip(model_dir=os.path.expanduser(argv['--model']))
    scan.scan_document(source=argv['SOURCE'], directory=argv['--out'], suffix='.bllip.xml',
                       fn=parse, non_sequences=[parser])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main(sys.argv[1:]))
