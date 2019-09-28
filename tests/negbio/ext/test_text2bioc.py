import os
import tempfile

import bioc

from negbio.ext.text2bioc import text2collection, printable, text2document, \
    text_to_collection_file


def test_printable():
    text = 'No pneumothorax.'
    actual = printable(text)
    assert actual == text

    actual = printable(text + '\b\n')
    assert actual == text + '\n'

    actual = printable(text + '\b\n', lambda x: x if x != '\b' else 'b')
    assert actual == text + 'b\n'


def test_text2document():
    def _helper(id, text, expected):
        d = text2document(id, text)
        assert d.id == id
        assert len(d.passages) == 1

        p = d.passages[0]
        assert p.text == expected

    id = 'id'
    text = 'No pneumothorax.'
    _helper(id, text, text)
    _helper(id, text + '\b\r\n', text+'\n')


def test_text2collection():
    text = 'No pneumothorax.'

    input = tempfile.mktemp()
    with open(input, 'w') as fp:
        fp.write(text)

    c = text2collection(input)
    assert len(c.documents) == 1

    d = c.documents[0]
    assert d.id == os.path.splitext(os.path.basename(input))[0]
    assert len(d.passages) == 1

    p = d.passages[0]
    assert p.text == text

    c = text2collection()
    assert len(c.documents) == 0

    c = text2collection(None)
    assert len(c.documents) == 0


def test_text_to_collection_file():
    text = 'No pneumothorax.'

    input = tempfile.mktemp()
    with open(input, 'w') as fp:
        fp.write(text)

    output = tempfile.mktemp()
    text_to_collection_file(output, input)
    with open(output) as fp:
        c = bioc.load(fp)
    assert c.documents[0].passages[0].text == text
