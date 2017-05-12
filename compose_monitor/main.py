import argparse

import os
import logging

import monitor


class StreamHandler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '%(asctime)s %(filename)s %(levelname)s: %(message)s'
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


class FileHandler(logging.FileHandler):

    def __init__(self, path):
        abspath = os.path.abspath(path)
        abspath_dir = re.search("^.+\/", abspath).group(0)
        if not os.path.exists(abspath_dir):
            os.makedirs(abspath_dir)
        if os.path.isdir(abspath):
            abspath = os.path.join(abspath, re.sub("py", "log", __file__))
        logging.FileHandler.__init__(self, abspath)
        fmt = '%(asctime)s %(filename)s %(levelname)s: %(message)s'
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--tag", dest="tag",
            default="latest", help="Tag name")
        parser.add_argument("-p", "--path", dest="path",
            default=".", help="Path to the docker-compose.yml")
        parser.add_argument("-o", "--options", dest="options",
            nargs='+', help="Options for project")
        parser.add_argument("-l", "--log", dest="log",
            help="Redirect logging to file")
        args = parser.parse_args()

        if args.log is not None:
            log = logging.getLogger(__name__)
            log.addHandler(FileHandler(args.log))
            log.setLevel(logging.DEBUG)
        else:
            log = logging.getLogger(__name__)
            log.addHandler(StreamHandler())
            log.setLevel(logging.DEBUG)

        if args.options is None:
            monitor = Monitor(args.path, {})
        else:
            monitor = Monitor(args.path,
                dict(zip(args.options[0::2], args.options[1::2])))

        monitor.run(10)

    except KeyboardInterrupt:
        print('\nThe process was interrupted by the user')
        raise SystemExit

main()
