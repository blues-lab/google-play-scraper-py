import subprocess
import json

class GooglePlayScraperException(Exception):
    pass

class GooglePlayScraper:
    script = (
        "var gplay = require('google-play-scraper'){};"
        "gplay.{}({{{}}})"
        ".then(JSON.stringify).then(console.log).catch(console.log);"
    )

    def __init__(self, memoization=False):
        self.memoization = '.memoized()' if memoization else ''

    def _execute(self, fn_name, keys, **kwargs):
        cmd = self._get_args(keys, **kwargs)
        script = self.script.format(self.memoization, fn_name, cmd)
        print(script)
        args = ['node', '-e', script]
        process = subprocess.run(args, capture_output=True, check=True)
        stdout, stderr = process.stdout.decode(), process.stderr.decode()
        try:
            return json.loads(stdout)
        except json.decoder.JSONDecodeError as e:
            raise GooglePlayScraperException(stdout) from None

    def _get_args(self, keys, **kwargs):
        stringify = lambda x: "'{}'".format(x) if isinstance(x, str) else '{}'.format(x)
        args = ', '.join(["{}: {}".format(k, stringify(v)) for k, v in kwargs.items() if k in keys + ['throttle']])
        return args

    def app(self, appId, **kwargs):
        keys = ['appId', 'lang', 'country']
        output = self._execute('app', keys, **{'appId': appId, **kwargs})
        return output

    def list(self, **kwargs):
        keys = [
            'collection', 'category', 'age', 'num',
            'lang', 'country', 'fullDetail'
        ]
        output = self._execute('list', keys, **kwargs)
        return output

    def search(self, term, **kwargs):
        keys = [
            'term', 'num', 'lang',
            'country', 'fullDetail', 'price'
        ]
        output = self._execute('search', keys,  **{'term': term, **kwargs})
        return output

    def developer(self, devId, **kwargs):
        keys = ['devId', 'lang', 'country', 'num', 'fullDetail']
        output = self._execute('developer', keys,  **{'devId': devId, **kwargs})
        return output

    def suggest(self, term, **kwargs):
        keys = ['term', 'lang', 'country']
        output = self._execute('suggest', keys,  **{'term': term, **kwargs})
        return output

    def reviews(self, appId, **kwargs):
        keys = [
            'appId', 'lang', 'country', 'sort',
            'num', 'paginate', 'nextPaginationToken'
        ]
        output = self._execute('reviews', keys,  **{'appId': appId, **kwargs})
        return output

    def similar(self, appId, **kwargs):
        keys = ['appId', 'lang', 'country', 'fullDetail']
        output = self._execute('similar', keys,  **{'appId': appId, **kwargs})
        return output

    def permissions(self, appId, **kwargs):
        keys = ['appId', 'lang', 'short']
        output = self._execute('permissions', keys,  **{'appId': appId, **kwargs})
        return output

    def categories(self, **kwargs):
        output = self._execute('categories', [],  **kwargs)
        return output

# 
# if __name__ == "__main__":
#
#     throttle = 1
#     scraper = GooglePlayScraper()
#
#     # app function.
#     # appId = 'com.google.android.apps.translate'
#     # lang = 'en'; country = 'us'
#     # output = scraper.app(appId=appId)#, lang=lang, country=country)
#
#     # list function.
#     output = scraper.list(lang='us', num=5, throttle=throttle)
#
#
#     print(output)
