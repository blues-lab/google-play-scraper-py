import subprocess
import json
import os
import logging

from .exceptions import ScraperException

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('__main__')

class Wrapper:

    # TODO: check that this is a valid path.
    require_dir = os.path.join(SELF_DIR, 'node_modules', 'google-play-scraper')

    api_script = (
        "var gplay = require('{}'){};"
        "gplay.{}({{{}}})"
        ".then(JSON.stringify).then(console.log).catch(console.log);"
    )

    var_script = (
        "var gplay = require('{}'){};"
        "let x = gplay.{};"
        "console.log(JSON.stringify(x));"
    )

    def __init__(self, memoization=False, vars=[]):
        self.memoization = '.memoized()' if memoization else ''
        for var in vars:
            setattr(Wrapper, var, self._execute_var(var))

    def _execute_api(self, fn_name, keys, **kwargs):
        cmd = self._get_args(keys, **kwargs)
        script = self.api_script.format(self.require_dir, self.memoization, fn_name, cmd)
        return self._execute(script)

    def _execute_var(self, var_name):
        script = self.var_script.format(self.require_dir, self.memoization, var_name)
        return self._execute(script)

    def _execute(self, script):
        logger.debug('Executing script: {}'.format(script))
        args = ['node', '-e', script]
        try:
            process = subprocess.run(args, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode()
            raise ScraperException(stderr) from None
        stdout = process.stdout.decode()
        try:
            return json.loads(stdout)
        except json.decoder.JSONDecodeError as e:
            raise ScraperException(stdout) from None

    def _get_args(self, keys, **kwargs):
        def stringify(x):
            if x is None:
                return 'null'
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
