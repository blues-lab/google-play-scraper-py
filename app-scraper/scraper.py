from wrapper import GooglePlayScraper, GooglePlayScraperException

class Scraper:

    def __init__(self):
        self.scraper = GooglePlayScraper(vars=['collection', 'category'])
        self.collections = list(self.scraper.collection.values())
        self.categories = list(self.scraper.category.values()) + ['OVERALL']

    def get_package_names(self, collections=[], categories=[], **kwargs):
        collections = self.collections if not collections else collections
        categories = self.categories if not categories else categories
        package_names = []
        for category in categories:
            for collection in collections:
                args = {
                    'collection': collection,
                    'category': category if category != 'OVERALL' else False, # check that it's equivalent
                    **kwargs
                }
                try:
                    result = self.scraper.list(**args)
                except GooglePlayScraperException as e: # TODO: log here...
                    continue
                package_names += [x['appId'] for x in result]
        return package_names

    def get_apps(self, package_names, **kwargs):
        apps = []
        for package_name in package_names:
            apps.append(self.scraper.app(appId=package_name, **kwargs))
        return apps
