
from negbio.pipeline import parse, ssplit, ptb2ud, negdetect, text2bioc, dner_mm, section_split, cleanup
from negbio.ext import normalize_mimiccxr


def process_collection(collection, metamap, splitter, parser, ptb2dep, lemmatizer, neg_detector, cuis, sec_title_patterns):
    for document in collection.documents:
        normalize_mimiccxr.normalize(document)
        section_split.split_document(document, sec_title_patterns)
        ssplit.ssplit(document, splitter)

    dner_mm.run_metamap_col(collection, metamap, cuis)

    for document in collection.documents:
        document = parse.parse(document, parser)
        document = ptb2ud.convert(document, ptb2dep, lemmatizer)
        document = negdetect.detect(document, neg_detector)
        cleanup.clean_sentences(document)

    return collection


def process_text(sources, metamap, splitter, parser, ptb2dep, lemmatizer, neg_detector, cuis, sec_title_patterns):
    collection = text2bioc.text2collection(*sources)
    return process_collection(collection, metamap, splitter, parser, ptb2dep, lemmatizer, neg_detector, cuis, sec_title_patterns)
