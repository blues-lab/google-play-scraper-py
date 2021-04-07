#!/usr/bin/env python3
import os
import sys
import json
import logging
import argparse
from appscraper.GooglePlayScraper import GooglePlayScraper

logger = logging.getLogger(__name__)

def _setup_logger():
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

class CommandLineTool:

    scraper = GooglePlayScraper()

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command', help='Subcommand to run')
        parser.add_argument('--output_path', '-o', help='')
        parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
        args = parser.parse_known_args()[0]
        logger_level = logging.DEBUG if args.verbose else logging.INFO
        logger.setLevel(logger_level)

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # Use dispatch pattern to invoke method with same name.
        results = getattr(self, args.command)()

        # Save output to file if provided or print to STDOUT.
        print(results) if args.output_path is None else self._save_results(results, args.output_path)

    def _save_results(self, results, output_path):
        with open(output_path, 'w') as f:
            json.dump(results, f)

    def app(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--appId', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.appId is not None, 'Must provide a valid Android App ID.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.app(**vargs)

    def list(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--collection', help='')
        parser.add_argument('--category', help='')
        parser.add_argument('--age', help='')
        parser.add_argument('--num', help='')
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--fullDetail', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.list(**vargs)

    def search(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--term', help='', required=True)
        parser.add_argument('--num', help='')
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--fullDetail', help='')
        parser.add_argument('--price', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.term is not None, 'Must provide a valid search term.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.search(**vargs)

    def developer(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--devId', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--num', help='')
        parser.add_argument('--fullDetail', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.devId is not None, 'Must provide a valid developer ID.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.developer(**vargs)

    def suggest(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--term', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.term is not None, 'Must provide a valid search term.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.suggest(**vargs)

    def reviews(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--appId', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--sort', help='')
        parser.add_argument('--num', help='')
        parser.add_argument('--paginate', help='')
        parser.add_argument('--nextPaginationToken', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.appId is not None, 'Must provide a valid Android App ID.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.reviews(**vargs)

    def similar(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--appId', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--country', help='')
        parser.add_argument('--fullDetail', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.appId is not None, 'Must provide a valid Android App ID.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.similar(**vargs)

    def permissions(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--appId', help='', required=True)
        parser.add_argument('--lang', help='')
        parser.add_argument('--short', help='')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert args.appId is not None, 'Must provide a valid Android App ID.'
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        return self.scraper.permissions(**vargs)

    def categories(self):
        return self.scraper.categories()

    def packages(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--collections', nargs='+', help='')
        parser.add_argument('--categories', nargs='+', help='')
        parser.add_argument('--num', default=200, type=int, help='Number of apps per category to scrape.')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        return self.scraper.get_package_names(**vars(args))

    def details(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('app_input_path', help='Path to file where app package names are located. Passing this argument scrapes only apps listed in the "input_path"')
        parser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        args = parser.parse_known_args()[0]
        assert os.path.isfile(args.app_input_path), 'Must specify path to valid file containing app package names.'

        with open(args.app_input_path, 'r') as f:
            data = f.read()
        try:
            package_names = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            package_names = data.rstrip().split('\n')
        return self.scraper.get_apps(package_names, **vars(args))

def main():
    _setup_logger()
    CommandLineTool()

if __name__ == "__main__":
    main()
