import logging


def clean_sentences(document, sort_anns=False):
    """
    Remove sentences in each passage

    Args:
        document(BioCDocument): a document
        sort_anns(bool): sort ann by its location
    """
    try:
        for passage in document.passages:
            del passage.sentences[:]

        if sort_anns:
            key_func = lambda ann: ann.get_total_location().offset
            id = 0
            for passage in document.passages:
                for ann in sorted(passage.annotations, key=key_func):
                    ann.id = str(id)
                    id += 1
    except:
        logging.exception("Cannot process %s", document.id)
    return document
