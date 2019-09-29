import logging
import re

from negbio.pipeline2.pipeline import Pipe


def pattern_repl(matchobj):
    """
    Replace [**Patterns**] with spaces.
    """
    s = matchobj.group(0).lower()
    return ' '.rjust(len(s))


def sub(text):
    text = re.sub(r'\[\*\*.*?\*\*\]', pattern_repl, text)
    text = re.sub(r'_', ' ', text)
    return text


def find_end(text):
    ends = [len(text)]
    patterns = [
        re.compile(r'BY ELECTRONICALLY SIGNING THIS REPORT', re.I),
        re.compile(r'\n {3,}DR.', re.I),
        re.compile(r'[ ]{1,}RADLINE ', re.I),
        re.compile(r'.*electronically signed on', re.I),
        re.compile(r'M\[0KM\[0KM')
    ]
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            ends.append(m.start())
    return min(ends)


def trim(text):
    text = sub(text)
    start = 0
    end = find_end(text)

    new_text = ''
    new_text += text[start:end]
    if len(text) - end > 0:
        new_text += ' ' * (len(text) - end)
    return new_text


class MIMICCXRNormalizer(Pipe):
    def __call__(self, doc, *args, **kwargs):
        try:
            if len(doc.passages) == 0:
                logging.warning('Skipped: there is no text in document %s', doc.id)
            elif len(doc.passages) > 1:
                logging.warning('Skipped: there is more than one passage in document %s', doc.id)
            else:
                doc.passages[0].text = trim(doc.passages[0].text)
            return doc
        except:
            logging.exception('Cannot find text in document %s', doc.id)
