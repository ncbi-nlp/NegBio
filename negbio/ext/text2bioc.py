import logging
import os
import string

import bioc


def printable(s, func=None):
    """
    Return string of ASCII string which is considered printable.

    Args:
        s(str): string
        func: function to convert non-ASCII characters
    """
    out = ''
    for c in s:
        if c in string.printable:
            out += c
        elif func is not None:
            out += func(c)
        else:
            logging.warning('Cannot convert char: %s', c)
    return out


def text2document(id, text):
    """
    Convert text to a BioCDocument instance

    Args:
        id (str): BioCDocument id
        text (str): text

    Returns:
        BioCDocument: a BioCDocument instance
    """
    document = bioc.BioCDocument()
    document.id = id
    text = printable(text).replace('\r\n', '\n')

    passage = bioc.BioCPassage()
    passage.offset = 0
    passage.text = text
    document.add_passage(passage)

    return document


def text2collection(*sources):
    """
    Returns a BioCCollection containing documents specified in sources.

    Args:
        sources: a list of pathname
    """
    collection = bioc.BioCCollection()
    for pathname in sources:
        logging.debug('Process %s', pathname)
        try:
            with open(pathname) as fp:
                text = fp.read()
            id = os.path.splitext(os.path.basename(pathname))[0]
            document = text2document(id, text)
            collection.add_document(document)
        except:
            logging.exception('Cannot convert %s', pathname)
    return collection


def text_to_collection_file(output, *file):
    """
    Convert text FILEs to the BioC output file

    Args:
        output: Specify the output file name.
        file: Specify the input text files
    """
    logging.basicConfig(level=logging.INFO)
    collection = text2collection(*file)
    with open(output, 'w') as fp:
        bioc.dump(collection, fp)
