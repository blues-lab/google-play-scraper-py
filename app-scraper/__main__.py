#!/usr/bin/env python3
import os
import sys
import json
import logging
import argparse
from scraper import Scraper

logger = logging.getLogger(__name__)

def _setup_logger(verbose=False):
    filename = 'output.log'
    datefmt = '%Y-%m-%d %H:%M:%S'
    log_format = '[%(asctime)s] - %(levelname)-8s %(message)s'
    formatter = logging.Formatter(log_format, datefmt)

    file_handler = logging.FileHandler(filename, 'w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.INFO)
    if verbose:
        logger.setLevel(logging.DEBUG)

class CommandLineTool:

    scraper = Scraper()
    output_path = None

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        results = getattr(self, args.command)()
        self._save_results(results)

    def _save_results(self, results):
        with open(self.output_path, 'w') as f:
            json.dump(results, f)

    def packages(self):
        parser = argparse.ArgumentParser()
        # prefixing the argument with -- means it's optional
        parser.add_argument('output_path', help='')
        parser.add_argument('--collections', nargs='+', help='')
        parser.add_argument('--categories', nargs='+', help='')
        parser.add_argument('--num', default=200, type=int, help='Number of apps per category to scrape.')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        self.output_path = args.output_path
        return self.scraper.get_package_names(**vars(args))

    def details(self):
        parser = argparse.ArgumentParser()
        # prefixing the argument with -- means it's optional
        parser.add_argument('app_input_path', default=None, help='Path to file where app package names are located. Passing this argument scrapes only apps listed in the "input_path"')
        parser.add_argument('output_path', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        self.output_path = args.output_path
        assert os.path.isfile(args.app_input_path), 'Must specify path to valid file containing app package names.'

        with open(args.app_input_path, 'r') as f:
            data = f.read()
        try:
            package_names = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            package_names = data.rstrip().split('\n')
        return self.scraper.get_apps(package_names, **vars(args))

def main():
    CommandLineTool()

if __name__ == "__main__":
    _setup_logger(verbose=False)
    main()
