import logging
import os

import docopt


__root__ = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))


def get_args(args):
    s = ''
    for k in args:
        s += '    {}: {}\n'.format(k, args[k])
    return s


def parse_args(doc, **kwargs):
    argv = docopt.docopt(doc, **kwargs)
    if argv['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug('Arguments:\n%s', get_args(argv))
    return argv


def get_absolute_path(argv, key, default_value):
    if argv[key] == default_value:
        argv[key] = os.path.join(__root__, argv[key])
    return argv


def calls_asynchronously(argv, cmd_prefix):
    import concurrent.futures
    from subprocess import call

    workers = int(argv.pop('--workers'))
    source = argv.pop('<file>')
    n = int(argv.pop('--files_per_worker'))
    output = argv.pop('--output')

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_cmd = {}
        for i in range(0, len(source), n):
            chunk = source[i:i + n]
            cmd = cmd_prefix
            # extra args
            for k, v in argv.items():
                if v is None:
                    continue
                elif isinstance(v, bool):
                    if v:
                        cmd += ' {}'.format(k)
                else:
                    cmd += ' {}={}'.format(k, v)
            # output and input
            cmd += ' --output={} {}'.format(output, ' '.join(chunk))
            logging.debug(cmd)
            future = executor.submit(call, cmd.split(' '))
            future_to_cmd[future] = cmd
        for future in concurrent.futures.as_completed(future_to_cmd):
            cmd = future_to_cmd[future]
            try:
                future.result()
            except Exception as exc:
                logging.exception('%r generated an exception: %s' % (cmd, exc))
