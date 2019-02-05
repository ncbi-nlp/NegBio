"""Define report loader class."""
import re

from negbio.pipeline.section_split import split_document


def _maketrans(s):
    s = s.replace(',', ', ')
    s = s.replace('.', '. ')
    return s


def extract_impression_from_passages(document):
    """Extract the Impression section from a Bioc Document."""
    document.passages = [passage for passage in document.passages
                         if passage.infons['title'] == "impression"]

    assert len(document.passages) <= 1, "The document contains {} impression passages.".format(len(document.passages))

    assert len(document.passages) >= 1, "The document contains no explicit impression passage."


class NegBioLoader(object):
    """Report impression loader."""
    def __init__(self, extract_impression=False):
        self.extract_impression = extract_impression
        # self.punctuation_spacer = string.maketrans({key: "{} ".format(key)
        #                                            for key in ".,"})
        # self.stop_spacer = string.maketrans('.', '. ')
        # self.comma_spacer = string.maketrans(',', ', ')

    def clean_doc(self, document):
        """Load and clean the reports."""
        for passage in document.passages:
            passage.text = self.clean(passage.text)

        if self.extract_impression:
            document = split_document(document)
            extract_impression_from_passages(document)

        return document

    def clean(self, report):
        """Clean the report text."""
        lower_report = report.lower()
        # Change `and/or` to `or`.
        corrected_report = re.sub('and/or',
                                  'or',
                                  lower_report)
        # Change any `XXX/YYY` to `XXX or YYY`.
        corrected_report = re.sub('(?<=[a-zA-Z])/(?=[a-zA-Z])',
                                  ' or ',
                                  corrected_report)
        # Clean double periods
        clean_report = corrected_report.replace("..", ".")
        # Insert space after commas and periods.
        clean_report = _maketrans(clean_report)
        # Convert any multi white spaces to single white spaces.
        clean_report = ' '.join(clean_report.split())

        return clean_report
