import filecmp
import os
import tempfile

import bioc
import pytest

from negbio.pipeline2.pipeline import NegBioPipeline, Pipe
from tests.negbio.utils import text_to_bioc


def create_collections():
    filenames = []
    top_dir = tempfile.mkdtemp()
    for i in range(10):
        c = text_to_bioc(['No pneumothorax.'], 'c/d/p')
        filename = os.path.join(top_dir, '{}.xml'.format(i))
        with open(filename, 'w') as fp:
            bioc.dump(c, fp)
        filenames.append(filename)
    return filenames


class FakePipe(Pipe):
    def __call__(self, doc: bioc.BioCDocument, *args, **kwargs):
        doc.infons['fake'] = True


def test_scan_collection():
    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    os.rmdir(output_dir)

    p = NegBioPipeline([('fake', FakePipe())])
    p.scan(source=filenames, directory=output_dir, suffix='.xml')
    for filename in filenames:
        filename = os.path.join(output_dir, os.path.basename(filename))
        with open(filename) as fp:
            c = bioc.load(fp)
            for doc in c.documents:
                assert doc.infons['fake']


def test_scan_collection_skip():
    filenames = create_collections()
    output_dir = tempfile.mkdtemp()
    # remove one file
    os.remove(filenames[0])

    p = NegBioPipeline([('fake', FakePipe())])
    p.scan(source=filenames, directory=output_dir, suffix='.xml')

    assert not os.path.exists(os.path.join(output_dir, filenames[0]))


def test_scan_document_return_none():
    class FakePipeNone(Pipe):
        def __call__(self, doc: bioc.BioCDocument, *args, **kwargs):
            return None

    filenames = create_collections()
    output_dir = tempfile.mkdtemp()

    p = NegBioPipeline([('fake_none', FakePipeNone())])
    p.scan(source=filenames, directory=output_dir, suffix='.xml')

    for filename in filenames:
        assert filecmp.cmp(filename, os.path.join(output_dir, os.path.basename(filename)))


def test_scan_document_error():
    class FakePipeError(Pipe):
        def __call__(self, doc: bioc.BioCDocument, *args, **kwargs):
            raise KeyError

    filenames = create_collections()
    output_dir = tempfile.mkdtemp()

    p = NegBioPipeline([('fake_error', FakePipeError())])
    p.scan(source=filenames, directory=output_dir, suffix='.xml')

    for filename in filenames:
        assert filecmp.cmp(filename, os.path.join(output_dir, os.path.basename(filename)))
