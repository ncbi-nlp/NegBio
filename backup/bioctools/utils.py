from __future__ import print_function

from builtins import str
import lxml.etree as etree
import bioc
from pynih.utils import terminated
from pynih import utils
from pynih.utils import terminated


def find_sentences(passage, loc):
    """
    Iteratively find the sentences in passage where the location falls in

    Args:
        passage(BioCPassage):
        loc(BioCLocation)
    
    Returns:
        BioCSentence
    """
    for sent in passage.sentences:
        if sent.offset <= loc.offset <= sent.offset + len(sent.text):
            yield sent
        elif sent.offset <= loc.offset + loc.length <= sent.offset + len(sent.text):
            yield sent


def find_sentence(passage, loc):
    """
    Find the sentence in passage where the location falls in
    
    Args:
        passage(BioCPassage)
        loc(BioCLocation)
    
    Returns:
        BioCSentence
    """
    for sent in passage.sentences:
        if sent.offset <= loc.offset and loc.offset + loc.length <= sent.offset + len(sent.text):
            return sent
    return None


def find_passage(collection, docid, offset):
    """
    Find the passage in collection with document id and offset

    Args:
        collection(BioCCollection)
        docid(str): document id
        offset(int)
        
    Returns:
        BioCPassage
    """
    for document in collection.documents:
        if document.id == docid:
            for passage in document.passages:
                if passage.offset == offset:
                    if not passage.text and len(passage.sentences) == 0:
                        continue
                    return passage
    return None


def intersect(ann1, ann2):
    loc1 = ann1.get_total_location()
    loc2 = ann2.get_total_location()
    return utils.intersect((loc1.offset, loc1.offset + loc1.length),
                           (loc2.offset, loc2.offset + loc2.length))


@terminated
def fill_char(text, offset, char='\n'):
    dis = offset - len(text)
    if dis > 0:
        text += char * dis
    return text


@terminated
def get_passage_text(passage):
    return get_text(passage)[1]


@terminated
def get_doc_text(document):
    return get_text(document)[1]


@terminated
def get_text(obj):
    """
    Return text with its offset in the document
    
    Args:
        obj: BioCDocument, BioCPassage, or BioCSentence
    
    Returns:
        tuple(int,str): offset, text
    """
    if isinstance(obj, bioc.BioCSentence):
        return obj.offset, obj.text,
    elif isinstance(obj, bioc.BioCPassage):
        if obj.text:
            return obj.offset, obj.text
        else:
            text = ''
            for sentence in obj.sentences:
                text = fill_char(text, sentence.offset - obj.offset, ' ')
                assert sentence.text, 'BioC sentence has no text: {}'.format(sentence.offset)
                text += sentence.text
            return obj.offset, text

    elif isinstance(obj, bioc.BioCDocument):
        text = ''
        for passage in obj.passages:
            text = fill_char(text, passage.offset)
            text += get_text(passage)[1]
        return 0, text
    else:
        raise ValueError('obj must be BioCCollection, BioCDocument, BioCPassage, or BioCSentence')


@terminated
def pretty_print(src, dst):
    """
    Pretty print the XML file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(src, parser)
    docinfo = tree.docinfo
    with open(dst, 'wb') as fp:
        fp.write(etree.tostring(tree, pretty_print=True,
                                encoding=docinfo.encoding, standalone=docinfo.standalone))


@terminated
def sort_document(src, dst):
    """
    Sort documents in a BioC collection based on document id.
    """
    with open(src) as fp:
        collection = bioc.load(fp)
    collection.documents = sorted(collection.documents, key=lambda d: d.id)
    with open(dst, 'w') as fp:
        bioc.dump(collection, fp)


@terminated
def add_annotation(passage, *annotations):
    """
    Replace passage's annotations (if any) with the new one.
    """
    id = 0
    del passage.annotations[:]
    for anns in annotations:
        for ann in anns:
            loc = ann.get_total_location()
            if passage.offset <= loc.offset \
                    and loc.offset + loc.length <= passage.offset + len(passage.text):
                ann.id = str(id)
                id += 1
                passage.add_annotation(ann)
    passage.annotations = sorted(passage.annotations, key=lambda ann: ann.get_total_location().offset)


@terminated
def get_annotations(collection, id):
    """
    Get all annotations in document id
    """
    annotations = []
    for document in collection.documents:
        if id == document.id:
            for passage in document.passages:
                annotations.extend(passage.annotations)
            return annotations
    return annotations
