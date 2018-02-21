"""
Convert from text to the BioC format

Usage:
    text2bioc [options] --out=DEST SOURCE ...

Options:
    --split-document    Split the document into passages based on section titles such as "Finding", "Impression" 
                        [default: True]
"""
from __future__ import print_function

import logging
import os
import re
import string
import sys

import bioc
import docopt

PATTERN = re.compile(r'(FINDINGS|COMPARISON|REASON FOR EXAM|EXAM|CLINICAL INDICATION|INDICATION'
                     r'|TECHNIQUE|IMPRESSION|HISTORY|REASON FOR STUDY'
                     r'|COMPARISON STUDY DATE|PROCEDURE|ABDOMEN AND PELVIS'
                     r'|EXAMINATION):',
                     re.IGNORECASE | re.MULTILINE)


def split_passage(text, offset=0):
    """
    Split the passages according to the pattern
    """

    def get_section(start, end):
        subtext = text[start:end]
        index = subtext.find(':')
        return subtext[:index] if index != -1 else None

    start = 0
    for matcher in PATTERN.finditer(text):
        logging.debug('Match: %s', matcher.group())
        end = matcher.start(1)
        if end == start:
            continue
        yield start + offset, end + offset, get_section(start, end)
        start = end
    end = len(text)
    # last piece
    yield start + offset, end + offset, get_section(start, end)


def printable(s, function=None):
    """
    Return string of ASCII string which is considered printable.

    Args:
        s(str): string
        function: function to convert non-ASCII characters
    """
    out = ''
    for c in s:
        if c in string.printable:
            out += c
        elif function:
            out += function
    return out


def text2document(id, text, split_document=True):
    """

    Args:
        id (str): BioCDocument id
        text (str): text
        split_document(bool): True if splits the passages according to the section titles.

    Returns:
        BioCDocument
    """
    document = bioc.BioCDocument()
    document.id = id
    text = printable(text).replace('\r\n', '\n')

    if split_document:
        last_section = None
        for start, end, section in split_passage(text):
            passage = bioc.BioCPassage()
            passage.offset = start
            passage.text = text[start:end]
            if section is None:
                section = last_section
            passage.infons['title'] = section
            document.add_passage(passage)
            last_section = section
    else:
        passage = bioc.BioCPassage()
        passage.offset = 0
        passage.text = text
        document.add_passage(passage)

    return document


def text2collection(*sources, **kwargs):
    """
    Returns a BioCCollection containing documents specified in sources.

    Args:
        split_document(bool): see text2document
    """
    split_document = kwargs.pop('split_document')

    collection = bioc.BioCCollection()
    for pathname in iter(*sources):
        with open(pathname) as fp:
            text = fp.read()
        id = os.path.splitext(os.path.basename(pathname))[0]
        document = text2document(id, text, split_document)
        collection.add_document(document)
    return collection


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)

    collection = text2collection(argv['SOURCE'], split_document=argv['--split-document'])
    with open(os.path.expanduser(argv['--out']), 'w') as fp:
        bioc.dump(collection, fp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    main(sys.argv[1:])
