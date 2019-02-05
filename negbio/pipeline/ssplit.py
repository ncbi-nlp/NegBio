import logging

import bioc


class NltkSSplitter(object):
    """NLTK sentence splitter"""

    def __init__(self, **kwargs):
        self.newline = kwargs.pop('newline', False)

    def split(self, text, **kwargs):
        import nltk
        if not text:
            return

        if self.newline:
            line_splitter = self.split_line
        else:
            line_splitter = self.no_split

        for line, line_offset in line_splitter(text):
            sent_list = nltk.sent_tokenize(line)
            offset = 0
            for sent in sent_list:
                offset = line.find(sent, offset)
                if offset == -1:
                    logging.debug('Cannot find {} in {}'.format(sent, text))
                yield sent, offset + line_offset
                offset += len(sent)

    @classmethod
    def split_line(cls, text, sep='\n'):
        lines = text.split(sep)
        offset = 0
        for line in lines:
            offset = text.index(line, offset)
            yield line, offset

    @classmethod
    def no_split(cls, text, **kwargs):
        yield text, 0

    def __repr__(self):
        return 'NLTK SSplitter'


class NegBioSSplitter(NltkSSplitter):
    def split_doc(self, document):
        """
        Split text into sentences with offsets.

        Args:v
            document(BioCDocument): one document

        Returns:
            BioCDocument
        """
        for passage in document.passages:
            for text, offset in self.split(passage.text):
                sentence = bioc.BioCSentence()
                sentence.offset = offset + passage.offset
                sentence.text = text
                passage.add_sentence(sentence)
            # passage.text = None
        return document
