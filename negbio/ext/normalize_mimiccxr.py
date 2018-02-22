"""
Usage:
    normalize_mimiccxr SRC DEST
"""

import sys
import os
import logging
import docopt
import re


def starrepl(matchobj):
    """
    Replace [**Patterns**] with spaces.
    """
    s = matchobj.group(0).lower()
    return ' '.rjust(len(s))
    # return matchobj.group(0).replace(' ', '@')


def sub(text):
    text = re.sub(r'\[\*\*.*?\*\*\]', starrepl, text)
    text = re.sub(r'_', ' ', text)
    return text


def find_start(text):
    return 0


def find_end(text):
    ends = [len(text)]
    patterns = [
        re.compile(r'BY ELECTRONICALLY SIGNING THIS REPORT', re.I),
        re.compile(r'\n         DR.', re.I),
        re.compile(r'[ ]{1,}RADLINE ', re.I),
        re.compile(r'.*electronically signed on', re.I),
        re.compile(r'M\[0KM\[0KM')
    ]
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            ends.append(m.start())
    return min(ends)


def trim(src, dst):
    with open(src) as fp:
        report = fp.read()

    report = sub(report)
    start = find_start(report)
    end = find_end(report)

    new_report = ''
    if start > 0:
        new_report += ' ' * start
    new_report += report[start:end]
    if len(report) - end > 0:
        new_report += ' ' * (len(report)-end)

    with open(dst, 'w') as fp:
        fp.write(new_report)


def main(argv):
    argv = docopt.docopt(__doc__, argv=argv)
    print(argv)
    trim(os.path.expanduser(argv['SRC']), os.path.expanduser(argv['DEST']))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
