from negbio.pipeline2.pipeline import Pipe


class CleanUp(Pipe):
    def __call__(self, doc, sort_anns=False, *args, **kwargs):
        """
        Remove sentences in each passage

        Args:
            document(BioCDocument): a document
            sort_anns(bool): sort ann by its location
        """
        for passage in doc.passages:
            del passage.sentences[:]

        if sort_anns:
            key_func = lambda ann: ann.total_span.offset
            id = 0
            for passage in doc.passages:
                passage.annotations = sorted(passage.annotations, key=key_func)
                for ann in passage.annotations:
                    ann.id = str(id)
                    id += 1
        return doc
