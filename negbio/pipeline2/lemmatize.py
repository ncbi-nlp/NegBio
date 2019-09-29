from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag.mapping import tagset_mapping

from negbio.pipeline2.pipeline import Pipe


class Lemmatizer(Pipe):
    def __init__(self):
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.mapping = tagset_mapping('en-ptb', 'universal')

    def lemmatize(self, word, pos=None):
        """
        Determines the lemma for a given word

        Args:
            word(str): word
            pos(str): part-of-speech

        Returns:
            str: lemma
        """
        if pos is not None:
            pos = self.map_tag(pos)

        if pos is not None:
            return self.wordnet_lemmatizer.lemmatize(word=word, pos=pos)
        else:
            return self.wordnet_lemmatizer.lemmatize(word=word)

    def map_tag(self, tag):
        """
        Convert POS from ptb to NLTK universal
        """
        if tag in self.mapping:
            tag = self.mapping[tag]
            if tag == 'NOUN':
                return wordnet.NOUN
            elif tag == 'VERB':
                return wordnet.VERB
            elif tag == 'ADJ':
                return wordnet.ADJ
            elif tag == 'ADV':
                return wordnet.ADV
            elif tag == 'ADJ_SAT':
                return wordnet.ADJ_SAT
        return None

    def __call__(self, doc, *args, **kwargs):
        for passage in doc.passages:
            for sentence in passage.sentences:
                for ann in sentence.annotations:
                    text = ann.text
                    pos = ann.infons['tag']
                    lemma = self.lemmatize(word=text, pos=pos)
                    ann.infons['lemma'] = lemma.lower()
        return doc
