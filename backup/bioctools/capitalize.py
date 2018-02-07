"""
Return a copy of src with only its first character capitalized
"""

import logging
import bioc
import re


PATTERN = re.compile('^( *)(.*)$')


def capitalize_s(s):
    """
    Return a copy of string with its first non-space character capitalized.
    """
    m = PATTERN.match(s)
    if m:
        return m.group(1) + m.group(2).capitalize()
    return s


def capitalize(src, dst):
    """
    Return a copy of src with only its first character capitalized
    """
    logger = logging.getLogger(__name__)

    with bioc.iterparse(src) as parser:
        with bioc.iterwrite(dst, parser.get_collection_info()) as writer:
            for document in parser:
                for passage in document.passages:
                    for sentence in passage.sentences:
                        if sentence.text:
                            sentence.text = capitalize_s(sentence.text)
                            logger.debug('{}: {}'.format(sentence.offset, sentence.text))
                writer.writedocument(document)
