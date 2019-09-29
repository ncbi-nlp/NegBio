import logging
import re
from typing import Pattern

import bioc

from negbio.pipeline2.pipeline import Pipe

SECTION_TITLES = re.compile(r'('
                            r'ABDOMEN AND PELVIS|CLINICAL HISTORY|CLINICAL INDICATION|COMPARISON|COMPARISON STUDY DATE'
                            r'|EXAM|EXAMINATION|FINDINGS|HISTORY|IMPRESSION|INDICATION'
                            r'|MEDICAL CONDITION|PROCEDURE|REASON FOR EXAM|REASON FOR STUDY|REASON FOR THIS EXAMINATION'
                            r'|TECHNIQUE'
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


class SectionSplitter(Pipe):
    def __init__(self, pattern: Pattern=None):
        """
        Args:
            pattern: the regular expression patterns for section titles.
        """
        if pattern is None:
            self.pattern = SECTION_TITLES
        else:
            self.pattern = pattern

    def __call__(self, doc, *args, **kwargs):
        """
        Split one report into sections. Section splitting is a deterministic consequence of section titles.

        Args:
            doc(BioCDocument): one document that contains one passage.

        Returns:
            BioCDocument: a new BioCDocument instance
        """
        new_document = bioc.BioCDocument()
        new_document.id = doc.id
        new_document.infons = doc.infons

        text = doc.passages[0].text
        offset = doc.passages[0].offset

        def create_passage(start, end, title=None):
            passage = bioc.BioCPassage()
            passage.offset = start + offset
            passage.text = text[start:end]
            if title is not None:
                passage.infons['title'] = title[:-1].strip() if title[-1] == ':' else title.strip()
                passage.infons['type'] = 'title_1'
            strip(passage)
            return passage

        start = 0
        for matcher in self.pattern.finditer(text):
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
