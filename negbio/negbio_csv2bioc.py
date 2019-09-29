"""
Convert text FILEs to the BioC output file

Usage:
    negbio_csv2bioc [options] --output=<directory> <file> ...

Options:
    --output=<dir>      Specify the output directory name.
    --verbose           Print more information about progress.
"""

import bioc
import collections
from negbio.cli_utils import parse_args
import tqdm
import pandas as pd
import hashlib
from pathlib import Path


def get_one_document(text):
    d = bioc.BioCDocument()
    p = bioc.BioCPassage()
    p.text = text
    p.offset = 0
    d.add_passage(p)
    return d


def csv2collections(dest_top, *sources):
    if not dest_top.exists():
        dest_top.mkdir(parents=True, exist_ok=True)
    total = collections.defaultdict(bioc.BioCCollection)
    for src in sources:
        all_df = pd.read_csv(src, header=None, names=['id', 'report'], )
        all_df = all_df.dropna()
        for i, row in tqdm.tqdm(all_df.iterrows(), total=len(all_df)):
            id = row['id']

            text = row['report']
            if text[0] == '"' and text[-1] == '"':
                text = text[1:-1]
            doc = get_one_document(text)
            doc.id = id

            col_id = hashlib.md5(id.encode()).hexdigest()[-2:]
            total[col_id].add_document(doc)

    for k, c in tqdm.tqdm(total.items(), total=len(total)):
        # print(len(c.documents))
        with open(dest_top / f'{k}.xml', 'w', encoding='utf8') as fp:
            bioc.dump(c, fp)


if __name__ == '__main__':
    argv = parse_args(__doc__)
    csv2collections(Path(argv['--output']), *argv['<file>'])

