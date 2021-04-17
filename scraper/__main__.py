#!/usr/bin/env python3
import os
import sys
import json
import logging
import argparse
import scraper.scraper

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
    handle = parser.add_subparsers(help='Command to pass to the Google Play Store scraper.', dest='command')

    # Create the parser for the 'app' command.
    subparsers['app'] = handle.add_parser('app', help='Retrieves the full detail of an application.')
    subparsers['app'].add_argument('appId', help='the Google Play id of the application (the ?id= parameter on the url).')
    subparsers['app'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code in which to fetch the app page.')
    subparsers['app'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the applications.')

    # Create the parser for the 'list' command.
    subparsers['list'] = handle.add_parser('list', help='Retrieves a list of applications from one of the collections at Google Play.')
    subparsers['list'].add_argument('--collection', help='(optional, defaults to collection.TOP_FREE): the Google Play collection that will be retrieved.')
    subparsers['list'].add_argument('--category', help='(optional, defaults to no category): the app category to filter by.')
    subparsers['list'].add_argument('--age', help='(optional, defaults to no age filter): the age range to filter the apps (only for FAMILY and its subcategories). Available options are age.FIVE_UNDER, age.SIX_EIGHT, age.NINE_UP.')
    subparsers['list'].add_argument('--num', help='(optional, defaults to 500): the amount of apps to retrieve.')
    subparsers['list'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code used to retrieve the applications.')
    subparsers['list'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the applications.')
    subparsers['list'].add_argument('--fullDetail', action='store_true', help='(optional, defaults to false): if true, an extra request will be made for every resulting app to fetch its full detail.')

    # Create the parser for the 'search' command.
    subparsers['search'] = handle.add_parser('search', help='Retrieves a list of apps that results of searching by the given term.')
    subparsers['search'].add_argument('term', help='the term to search by.')
    subparsers['search'].add_argument('--num', help='(optional, defaults to 20, max is 250): the amount of apps to retrieve.')
    subparsers['search'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code used to retrieve the applications.')
    subparsers['search'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the applications.')
    subparsers['search'].add_argument('--fullDetail', action='store_true', help='(optional, defaults to false): if true, an extra request will be made for every resulting app to fetch its full detail.')
    subparsers['search'].add_argument('--price', help='(optional, defaults to all): allows to control if the results apps are free, paid or both. Accepted values are: \'all\', \'free\' and \'paid\'.')

    # Create the parser for the 'developer' command.
    subparsers['developer'] = handle.add_parser('developer', help='Returns the list of applications by the given developer name.')
    subparsers['developer'].add_argument('devId', help='the name of the developer.')
    subparsers['developer'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code in which to fetch the app list.')
    subparsers['developer'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the applications. Needed when the app is available only in some countries.')
    subparsers['developer'].add_argument('--num', help='(optional, defaults to 60): the amount of apps to retrieve.')
    subparsers['developer'].add_argument('--fullDetail', action='store_true', help='(optional, defaults to false): if true, an extra request will be made for every resulting app to fetch its full detail.')

    # Create the parser for the 'suggest' command.
    subparsers['suggest'] = handle.add_parser('suggest', help='Given a string returns up to five suggestion to complete a search query term.')
    subparsers['suggest'].add_argument('term', help='the term to get suggestions for.')
    subparsers['suggest'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code used to retrieve the suggestions.')
    subparsers['suggest'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the suggestions.')

    # Create the parser for the 'reviews' command.
    subparsers['reviews'] = handle.add_parser('reviews', help='Retrieves a page of reviews for a specific application.')
    subparsers['reviews'].add_argument('appId', help='Unique application id for Google Play. (e.g. id=com.mojang.minecraftpe maps to Minecraft: Pocket Edition game).')
    subparsers['reviews'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code in which to fetch the reviews.')
    subparsers['reviews'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code in which to fetch the reviews.')
    subparsers['reviews'].add_argument('--sort', help='(optional, defaults to sort.NEWEST): The way the reviews are going to be sorted. Accepted values are: sort.NEWEST, sort.RATING and sort.HELPFULNESS.')
    subparsers['reviews'].add_argument('--num', help='(optional, defaults to 100): Quantity of reviews to be captured.')
    subparsers['reviews'].add_argument('--paginate', help='(optional, defaults to false): Defines if the result will be paginated')
    subparsers['reviews'].add_argument('--nextPaginationToken', help='(optional, defaults to null): The next token to paginate')

    # Create the parser for the 'similar' command.
    subparsers['similar'] = handle.add_parser('similar', help='Returns a list of similar apps to the one specified.')
    subparsers['similar'].add_argument('appId', help='the Google Play id of the application to get similar apps for.')
    subparsers['similar'].add_argument('--lang', help='(optional, defaults to \'en\'): the two letter language code used to retrieve the applications.')
    subparsers['similar'].add_argument('--country', help='(optional, defaults to \'us\'): the two letter country code used to retrieve the applications.')
    subparsers['similar'].add_argument('--fullDetail', action='store_true', help='(optional, defaults to false): if true, an extra request will be made for every resulting app to fetch its full detail.')

    # Create the parser for the 'permissions' command.
    subparsers['permissions'] = handle.add_parser('permissions', help='Returns the list of permissions an app has access to.')
    subparsers['permissions'].add_argument('appId', help='the Google Play id of the application to get permissions for.')
    subparsers['permissions'].add_argument('--lang',  help='(optional, defaults to \'en\'): the two letter language code in which to fetch the permissions.')
    subparsers['permissions'].add_argument('--short', action='store_true', help='(optional, defaults to false): if true, the permission names will be returned instead of permission/description objects.')

    # Create the parser for the 'categories' command.
    subparsers['categories'] = handle.add_parser('categories', help='Retrieve a full list of categories present from dropdown menu on Google Play.')

    # Add universal commands to all subparsers.
    for subparser in subparsers.values():
        subparser.add_argument('--output_path', '-o', help='')
        subparser.add_argument('--throttle', default=1, type=int, help='Upper bound to the amount of requests that will be attempted per second.')
        subparser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    return parser, subparsers

class CommandLineTool:

    def __init__(self, parser):
        args = parser.parse_args()

        wrapper_fns = [x for x in dir(scraper) if callable(getattr(scraper, x))]
        wrapper_fns = [x for x in wrapper_fns if len(x) > 0 and x[0] != '_']
        vargs = {k:v for k, v in vars(args).items() if v is not None}

        # Check if the supplied command is valid.
        if args.command is None or not hasattr(scraper, args.command):
            print('Unrecognized command: {}.'.format(args.command))
            parser.print_help()
            exit(1)

        logger.setLevel(logging.DEBUG) if args.verbose else logger.setLevel(logging.INFO)
        results = getattr(scraper, args.command)(**vargs)

        # Save output to file if provided or print to STDOUT.
        print(results) if args.output_path is None else self._save_results(results, args.output_path)

    def _save_results(self, results, output_path):
        with open(output_path, 'w') as f:
            json.dump(results, f)

def main():
    _setup_logger()
    parser, subparsers = _setup_parsers()
    CommandLineTool(parser)

if __name__ == "__main__":
    main()
