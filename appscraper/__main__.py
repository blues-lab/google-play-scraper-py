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

def _setup_parsers():
    # Create the top-level parser.
    parser, subparsers = argparse.ArgumentParser(), {}
    handle = parser.add_subparsers(help='sub-command help', dest='command')

    # Create the parser for the 'app' command.
    subparsers['app'] = handle.add_parser('app', help='Retrieves the full detail of an application.')
    subparsers['app'].add_argument('appId', help='the Google Play id of the application (the ?id= parameter on the url).')
    subparsers['app'].add_argument('--lang', help='(optional, defaults to "en"): the two letter language code in which to fetch the app page.')
    subparsers['app'].add_argument('--country', help='')

    # Create the parser for the 'list' command.
    subparsers['list'] = handle.add_parser('list', help='Retrieves a list of applications from one of the collections at Google Play.')
    subparsers['list'].add_argument('--collection', help='')
    subparsers['list'].add_argument('--category', help='')
    subparsers['list'].add_argument('--age', help='')
    subparsers['list'].add_argument('--num', help='')
    subparsers['list'].add_argument('--lang', help='')
    subparsers['list'].add_argument('--country', help='')
    subparsers['list'].add_argument('--fullDetail', help='')

    # Create the parser for the 'search' command.
    subparsers['search'] = handle.add_parser('search', help='Retrieves a list of apps that results of searching by the given term.')
    subparsers['search'].add_argument('term', help='')
    subparsers['search'].add_argument('--num', help='')
    subparsers['search'].add_argument('--lang', help='')
    subparsers['search'].add_argument('--country', help='')
    subparsers['search'].add_argument('--fullDetail', help='')
    subparsers['search'].add_argument('--price', help='')

    # Create the parser for the 'developer' command.
    subparsers['developer'] = handle.add_parser('developer', help='Returns the list of applications by the given developer name.')
    subparsers['developer'].add_argument('devId', help='')
    subparsers['developer'].add_argument('--lang', help='')
    subparsers['developer'].add_argument('--country', help='')
    subparsers['developer'].add_argument('--num', help='')
    subparsers['developer'].add_argument('--fullDetail', help='')

    # Create the parser for the 'suggest' command.
    subparsers['suggest'] = handle.add_parser('suggest', help='Given a string returns up to five suggestion to complete a search query term.')
    subparsers['suggest'].add_argument('term', help='')
    subparsers['suggest'].add_argument('--lang', help='')
    subparsers['suggest'].add_argument('--country', help='')

    # Create the parser for the 'reviews' command.
    subparsers['reviews'] = handle.add_parser('reviews', help='Retrieves a page of reviews for a specific application.')
    subparsers['reviews'].add_argument('appId', help='')
    subparsers['reviews'].add_argument('--lang', help='')
    subparsers['reviews'].add_argument('--country', help='')
    subparsers['reviews'].add_argument('--sort', help='')
    subparsers['reviews'].add_argument('--num', help='')
    subparsers['reviews'].add_argument('--paginate', help='')
    subparsers['reviews'].add_argument('--nextPaginationToken', help='')

    # Create the parser for the 'similar' command.
    subparsers['similar'] = handle.add_parser('similar', help='Returns a list of similar apps to the one specified.')
    subparsers['similar'].add_argument('appId', help='')
    subparsers['similar'].add_argument('--lang', help='')
    subparsers['similar'].add_argument('--country', help='')
    subparsers['similar'].add_argument('--fullDetail', help='')

    # Create the parser for the 'permissions' command.
    subparsers['permissions'] = handle.add_parser('permissions', help='Returns the list of permissions an app has access to.')
    subparsers['permissions'].add_argument('appId', help='the Google Play id of the application (the ?id= parameter on the url).')
    subparsers['permissions'].add_argument('--lang',  help='')
    subparsers['permissions'].add_argument('--short', help='')

    # Create the parser for the 'categories' command.
    subparsers['categories'] = handle.add_parser('categories', help='Retrieve a full list of categories present from dropdown menu on Google Play.')

    # Add universal commands to all subparsers.
    for subparser in subparsers.values():
        subparser.add_argument('--output_path', '-o', help='')
        subparser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        subparser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    return parser.parse_args()

class CommandLineTool:

    scraper = GooglePlayScraper()

    def __init__(self, args):
        output_path = args.output_path
        logger.setLevel(logging.DEBUG) if args.verbose else logger.setLevel(logging.INFO)

        wrapper_fns = [x for x in dir(GooglePlayScraper) if callable(getattr(GooglePlayScraper, x))]
        wrapper_fns = [x for x in wrapper_fns if len(x) > 0 and x[0] != '_']
        vargs = {k:v for k, v in vars(args).items() if v is not None}
        results = getattr(self.scraper, args.command)(**vargs)

        # Save output to file if provided or print to STDOUT.
        print(results) if output_path is None else self._save_results(results, args.output_path)

    def _save_results(self, results, output_path):
        with open(output_path, 'w') as f:
            json.dump(results, f)

def main():
    _setup_logger()
    CommandLineTool(_setup_parsers())

if __name__ == "__main__":
    main()
