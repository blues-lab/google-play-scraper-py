from appscraper.GooglePlayScraperWrapper import GooglePlayScraperWrapper, GooglePlayScraperException

class GooglePlayScraper:

    def __init__(self):
        self.scraper = GooglePlayScraperWrapper(vars=['collection', 'category'])
        self.playstore_collections = list(self.scraper.collection.values())
        self.playstore_categories = list(self.scraper.category.values()) + ['OVERALL']

    def app(self, appId, **kwargs):
        return self.scraper.app(appId, **kwargs)

    def list(self, **kwargs):
        return self.scraper.list(**kwargs)

    def search(self, term, **kwargs):
        return self.scraper.search(term, **kwargs)

    def developer(self, devId, **kwargs):
        return self.scraper.developer(devId, **kwargs)

    def suggest(self, term, **kwargs):
        return self.scraper.suggest(term, **kwargs)

    def reviews(self, appId, **kwargs):
        return self.scraper.reviews(term, **kwargs)

    def similar(self, appId, **kwargs):
        return self.scraper.similar(appId, **kwargs)

    def permissions(self, appId, **kwargs):
        return self.scraper.permissions(appId, **kwargs)

    def categories(self, **kwargs):
        return self.scraper.categories(**kwargs)

    def packages(self, collections=[], categories=[], **kwargs):
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

    def details(self, package_names, **kwargs):
        apps = []
        for package_name in package_names:
            apps.append(self.scraper.app(appId=package_name, **kwargs))
        return apps
