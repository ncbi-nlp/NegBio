import logging
import dcache
import tqdm
import os


def scan(*_, **kwargs):
    """
    This function constructs and applies a Scan op to the provided
    arguments.
    Parameters
    ----------
    fn
        ``fn`` is a function that describes the operations involved in one
        step of ``scan``. ``fn`` should construct variables describing the
        output of one iteration step. It should expect as input
        variables representing all the slices of the input sequences,
        as well as all other arguments
        given to scan as ``non_sequences``. The order in which scan passes
        these variables to ``fn``  is the following :
        * all time slices of the first sequence
        * all time slices of the second sequence
        * ...
        * all time slices of the last sequence
        * all other arguments (the list given as `non_sequences` to
            scan)
    """
    start = kwargs.pop('start', None)
    stop = kwargs.pop('stop', None)
    fn = kwargs.pop('fn')
    sequences = kwargs.pop('sequences')
    non_sequences = kwargs.pop('non_sequences', None)

    if len(sequences) <= 0:
        raise ValueError("Need at least one sequence")

    if start is None:
        start = 0
    if stop is None:
        stop = len(sequences[0])

    for t, seqst in enumerate(zip(*sequences)):
        if t < start or t >= stop:
            continue
        args = list(seqst)
        if non_sequences is not None:
            args += non_sequences
        logging.info('Process %s', args[0])
        try:
            fn(*args)
        except:
            logging.exception('Cannot process %s', args[0])


def scan_dcache(*_, **kwargs):
    """
    fn should expect the following arguments in this given order:
        sequence1
        sequence2
        ...
        non_sequence1
        non_sequence2
        ...
    """
    cache_file = kwargs.pop('cache_file')
    start = kwargs.pop('start')
    stop = kwargs.pop('stop', None)
    fn = kwargs.pop('fn')
    suffixes = kwargs.pop('suffixes')
    non_sequences = kwargs.pop('non_sequences', None)

    start = int(start)
    stop = int(stop)

    cache = dcache.load(cache_file)
    subcache = dcache.sub(cache, start, stop)
    sequences = []
    for s in suffixes:
        args = [subcache.filename(item, suffix=s) for item in subcache]
        sequences.append(args)
    return scan(fn=fn, sequences=sequences, non_sequences=non_sequences)


def scan_document(fn, directory, siffix, verbose=True, *source):
    """
    Args:
        source(list): a list of source pathnames
        directory(str): output directory
        fn:
            fn should expect the following arguments in this given order:
                sequence1
                sequence2
                ...
                non_sequence1
                non_sequence2
                ...
    """
    for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose):
        basename = os.path.splitext(os.path.basename(pathname))[0]
        dstname = os.path.join(directory, '{}.{}'.format(basename, suffix))
        with open(pathname) as fp:
            collection = bioc.load(fp)
            for document in collection.documents:
                ssplit(splitter, document)
        with open(dstname, 'w') as fp:
            bioc.dump(collection, fp)
