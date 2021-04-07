import subprocess
import json
import os
import logging

WORK_DIR, SELF_DIR = os.getcwd(), os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('__main__')

class GooglePlayScraperException(Exception):
    pass

class GooglePlayScraperWrapper:
    api_script = (
        "var gplay = require('google-play-scraper'){};"
        "gplay.{}({{{}}})"
        ".then(JSON.stringify).then(console.log).catch(console.log);"
    )

    var_script = (
        "var gplay = require('google-play-scraper'){};"
        "let x = gplay.{};"
        "console.log(JSON.stringify(x));"
    )

    def __init__(self, memoization=False, vars=[]):
        self.memoization = '.memoized()' if memoization else ''
        for var in vars:
            setattr(GooglePlayScraperWrapper, var, self._execute_var(var))

    def _execute_api(self, fn_name, keys, **kwargs):
        cmd = self._get_args(keys, **kwargs)
        script = self.api_script.format(self.memoization, fn_name, cmd)
        return self._execute(script)

    def _execute_var(self, var_name):
        script = self.var_script.format(self.memoization, var_name)
        return self._execute(script)

    def _execute(self, script):
        logger.debug('Executing script: {}'.format(script))
        args = ['node', '-e', script]
        try:
            os.chdir(SELF_DIR)
            process = subprocess.run(args, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise GooglePlayScraperException(e) from None
        finally:
            os.chdir(WORK_DIR)
        stdout, stderr = process.stdout.decode(), process.stderr.decode()
        try:
            return json.loads(stdout)
        except json.decoder.JSONDecodeError as e:
            raise GooglePlayScraperException(stdout) from None

    def _get_args(self, keys, **kwargs):
        def stringify(x):
            if isinstance(x, str):
                return "'{}'".format(x)
            elif type(x) == bool:
                return '{}'.format(str(x).lower())
            return '{}'.format(x)

        args = ', '.join(["{}: {}".format(k, stringify(v)) for k, v in kwargs.items() if k in keys + ['throttle']])
        return args

    def app(self, appId, **kwargs):
        keys = ['appId', 'lang', 'country']
        output = self._execute_api('app', keys, **{'appId': appId, **kwargs})
        return output

    def list(self, **kwargs):
        keys = [
            'collection', 'category', 'age', 'num',
            'lang', 'country', 'fullDetail'
        ]
        output = self._execute_api('list', keys, **kwargs)
        return output

    def search(self, term, **kwargs):
        keys = [
            'term', 'num', 'lang',
            'country', 'fullDetail', 'price'
        ]
        output = self._execute_api('search', keys,  **{'term': term, **kwargs})
        return output

    def developer(self, devId, **kwargs):
        keys = ['devId', 'lang', 'country', 'num', 'fullDetail']
        output = self._execute_api('developer', keys,  **{'devId': devId, **kwargs})
        return output

    def suggest(self, term, **kwargs):
        keys = ['term', 'lang', 'country']
        output = self._execute_api('suggest', keys,  **{'term': term, **kwargs})
        return output

    def reviews(self, appId, **kwargs):
        keys = [
            'appId', 'lang', 'country', 'sort',
            'num', 'paginate', 'nextPaginationToken'
        ]
        output = self._execute_api('reviews', keys,  **{'appId': appId, **kwargs})
        return output

    def similar(self, appId, **kwargs):
        keys = ['appId', 'lang', 'country', 'fullDetail']
        output = self._execute_api('similar', keys,  **{'appId': appId, **kwargs})
        return output

    def permissions(self, appId, **kwargs):
        keys = ['appId', 'lang', 'short']
        output = self._execute_api('permissions', keys,  **{'appId': appId, **kwargs})
        return output

    def categories(self, **kwargs):
        output = self._execute_api('categories', [],  **kwargs)
        return output
