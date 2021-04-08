from appscraper.GooglePlayScraperWrapper import GooglePlayScraperWrapper, GooglePlayScraperException

class GooglePlayScraper:

    def __init__(self):
        self.scraper = GooglePlayScraperWrapper(vars=['collection', 'category', 'age', 'sort'])

    # TODO: check that the default values in python produce the same outputs as the default values in the JavaScript API

    def app(self, appId, lang='en', country='us', **kwargs):
        return self.scraper.app(appId, **kwargs)

    # TODO: try none or false for none defaults
    def list(self, collection=None, category=None, age=None, num=500, lang='en', country='us', fullDetail=False, **kwargs):
        collection = self.scraper.collection['TOP_FREE'] if collection is None else collection
        vargs = {
            'collection': self.scraper.collection['TOP_FREE'] if collection is None else collection,
            'category': category,
            'age': age,
            'num': num,
            'lang': lang,
            'country': country,
            'fullDetail': fullDetail,
            **kwargs
        }
        return self.scraper.list(**vargs)

    def search(self, term, num=20, lang='en', country='us', fullDetail=False, price='all', **kwargs):
        vargs = {
            'term': term,
            'num': num,
            'lang': lang,
            'country': country,
            'fullDetail': fullDetail,
            'price': price,
            **kwargs
        }
        return self.scraper.search(**vargs)

    def developer(self, devId, lang='en', country='us', num=60, fullDetail=False, **kwargs):
        vargs = {
            'devId': devId,
            'lang': lang,
            'country': country,
            'num': num,
            'fullDetail': fullDetail,
            **kwargs
        }
        return self.scraper.developer(**vargs)

    def suggest(self, term, lang='en', country='us', **kwargs):
        vargs = {
            'term': term,
            'lang': lang,
            'country': country,
            **kwargs
        }
        return self.scraper.suggest(**vargs)

    def reviews(self, appId, lang='en', country='us', sort=None, num=100, paginate=False, nextPaginationToken=None, **kwargs):
        vargs = {
            'appId': appId,
            'lang': lang,
            'country': country,
            'sort': self.scraper.sort['NEWEST'] if sort is None else sort,
            'num': num,
            'paginate': paginate,
            'nextPaginationToken': nextPaginationToken,
            **kwargs
        }
        return self.scraper.reviews(**vargs)

    def similar(self, appId, lang='en', country='us', fullDetail=False, **kwargs):
        vargs = {
            'appId': appId,
            'lang': lang,
            'country': country,
            'fullDetail': fullDetail,
            **kwargs
        }
        return self.scraper.similar(**vargs)

    def permissions(self, appId, lang='en', short=False, **kwargs):
        vargs = {
            'appId': appId,
            'lang': lang,
            'short': short,
            **kwargs
        }
        return self.scraper.permissions(**vargs)

    def categories(self, **kwargs):
        return self.scraper.categories(**kwargs)

    # def packages(self, collections=[], categories=[], **kwargs):
    #     collections = self.collections if not collections else collections
    #     categories = self.categories if not categories else categories
    #     package_names = []
    #     for category in categories:
    #         for collection in collections:
    #             args = {
    #                 'collection': collection,
    #                 'category': category if category != 'OVERALL' else False, # check that it's equivalent
    #                 **kwargs
    #             }
    #             try:
    #                 result = self.scraper.list(**args)
    #             except GooglePlayScraperException as e: # TODO: log here...
    #                 continue
    #             package_names += [x['appId'] for x in result]
    #     return package_names
    #
    # def details(self, package_names, **kwargs):
    #     apps = []
    #     for package_name in package_names:
    #         apps.append(self.scraper.app(appId=package_name, **kwargs))
    #     return apps
