import logging
import re

import bioc

SECTION_TITLES = re.compile(r'('
                            r'ABDOMEN AND PELVIS|CLINICAL HISTORY|CLINICAL INDICATION|COMPARISON|COMPARISON STUDY DATE'
                            r'|EXAM|EXAMINATION|FINDINGS|HISTORY|IMPRESSION|INDICATION'
                            r'|MEDICAL CONDITION|PROCEDURE|REASON FOR EXAM|REASON FOR STUDY|TECHNIQUE'
                            r'):|FINAL REPORT',
                            re.IGNORECASE | re.MULTILINE)


def is_empty(passage):
    return len(passage.text) == 0


def strip(passage):
    start = 0
    while start < len(passage.text) and passage.text[start].isspace():
        start += 1

    end = len(passage.text)
    while end > start and passage.text[end - 1].isspace():
        end -= 1

    passage.offset += start
    logging.debug('before: %r' % passage.text)
    passage.text = passage.text[start:end]
    logging.debug('after:  %r' % passage.text)
    return passage


def split_document(document):
    """
    Split one report into sections. Section splitting is a deterministic consequence of section titles.

    Args:
        document(BioCDocument): one document that contains one passage.

    Returns:
        BioCDocument: a new BioCDocument instance
    """
    new_document = bioc.BioCDocument()
    new_document.id = document.id
    new_document.infons = document.infons

    text = document.passages[0].text
    offset = document.passages[0].offset

    def create_passage(start, end, title=None):
        passage = bioc.BioCPassage()
        passage.offset = start + offset
        passage.text = text[start:end]
        if title is not None:
            passage.infons['title'] = title[:-1].strip() if title[-1] == ':' else title.strip()
        strip(passage)
        return passage

    start = 0
    for matcher in SECTION_TITLES.finditer(text):
        logging.debug('Match: %s', matcher.group())
        # add last
        end = matcher.start()
        if end != start:
            passage = create_passage(start, end)
            if not is_empty(passage):
                new_document.add_passage(passage)

        start = end

        # add title
        end = matcher.end()
        passage = create_passage(start, end, text[start:end])
        if not is_empty(passage):
            new_document.add_passage(passage)

        start = end

    # add last piece
    end = len(text)
    if start < end:
        passage = create_passage(start, end)
        if not is_empty(passage):
            new_document.add_passage(passage)
    return new_document


def split_collection(collection):
    for i in range(len(collection.documents)):
        document = collection.documents[i]
        try:
            if len(document.passages) == 0:
                logging.warning('Skipped: there is no text in document %s', document.id)
            elif len(document.passages) > 1:
                logging.warning('Skipped: there is more than one passage in document %s', document.id)
            else:
                collection.documents[i] = split_document(document)
        except:
            logging.exception('Cannot find text in document %s', document.id)
    return collection
