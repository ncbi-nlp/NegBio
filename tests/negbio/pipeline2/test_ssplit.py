import pytest

from negbio.pipeline2.ssplit import NegBioSSplitter
from tests.negbio.utils import text_to_bioc


@pytest.fixture(scope='module')
def splitter():
    return NegBioSSplitter()


class TestNegBioSSplitter:
    def test_split(self, splitter):
        text = 'No pneumothorax. No pneumothorax.'
        rst = [(line, offset) for line, offset in splitter.split(text)]
        assert len(rst) == 2
        assert rst[0][0] == 'No pneumothorax.'
        assert rst[0][1] == 0
        assert rst[1][0] == 'No pneumothorax.'
        assert rst[1][1] == 17

        rst = [(line, offset) for line, offset in splitter.split('')]
        assert len(rst) == 0
        rst = [(line, offset) for line, offset in splitter.split(None)]
        assert len(rst) == 0

    def test_init(self):
        ssplit = NegBioSSplitter(newline=True)
        text = 'No pneumothorax \nNo pneumothorax.'
        rst = [(line, offset) for line, offset in ssplit.split(text)]
        assert len(rst) == 2

        ssplit = NegBioSSplitter()
        text = 'No pneumothorax \nNo pneumothorax.'
        rst = [(line, offset) for line, offset in ssplit.split(text)]
        assert len(rst) == 1

    def test_split_line(self, splitter):
        text = 'No pneumothorax.\nNo pneumothorax.'
        rst = [(line, offset) for line, offset in splitter.split_line(text)]
        assert len(rst) == 2
        assert rst[0][0] == 'No pneumothorax.'
        assert rst[0][1] == 0
        assert rst[1][0] == 'No pneumothorax.'
        assert rst[1][1] == 17

        text = 'No pneumothorax. No pneumothorax.'
        rst = [(line, offset) for line, offset in splitter.split_line(text)]
        assert len(rst) == 1
        assert rst[0][0] == text
        assert rst[0][1] == 0

    def test_no_split(self, splitter):
        text = 'hello world!\nhello world!'
        rst = [(line, offset) for line, offset in splitter.no_split(text)]
        assert len(rst) == 1
        assert rst[0][0] == text
        assert rst[0][1] == 0

    def test_split_doc(self, splitter):
        text = 'No pneumothorax.\nNo pneumothorax.'
        document = text_to_bioc([text], 'd/p')
        p = document.passages[0]
        assert p.text == text
        assert len(p.sentences) == 0

        document = splitter.__call__(document)
        p = document.passages[0]
        assert len(p.sentences) == 2
        assert p.sentences[0].text == 'No pneumothorax.'
        assert p.sentences[0].offset == 0
        assert p.sentences[1].text == 'No pneumothorax.'
        assert p.sentences[1].offset == 17
