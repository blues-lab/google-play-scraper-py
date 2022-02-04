import subprocess
import json
import os
import logging

from .exceptions import ScraperException

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_DIR = os.path.join(SELF_DIR, 'node_modules', 'google-play-scraper')
logger = logging.getLogger('__main__')

# Private module class.
class _Wrapper:

    node_dir = [x if x != '' else os.path.sep for x in NODE_DIR.split(os.path.sep)]
    require_dir = "'{}'".format("', '".join(node_dir))

    api_script = (
        "var gplay = require(path.join({})){};"
        "gplay.{}({{{}}})"
        ".then(JSON.stringify).then(console.log).catch(console.log);"
    )

    var_script = (
        "var gplay = require(path.join({})){};"
        "let x = gplay.{};"
        "console.log(JSON.stringify(x));"
    )

    def __init__(self, memoization=False, vars=[]):
        self.memoization = '.memoized()' if memoization else ''
        for var in vars:
            setattr(_Wrapper, var, self._execute_var(var))

    def _execute_api(self, fn_name, keys, **kwargs):
        cmd = self._get_args(keys, **kwargs)
        script = self.api_script.format(
            self.require_dir, self.memoization, fn_name, cmd)
        return self._execute(script)

    def _execute_var(self, var_name):
        script = self.var_script.format(
            self.require_dir, self.memoization, var_name)
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
        except json.decoder.JSONDecodeError:
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

        args = ', '.join(["{}: {}".format(k, stringify(v))
                          for k, v in kwargs.items() if k in keys + ['throttle']])
        return args


# Private module attributes.
_wrapper = _Wrapper(vars=['collection', 'category', 'age', 'sort'])

# Public module attributes.
collection = _wrapper.collection
category = _wrapper.category
age = _wrapper.age
sort = _wrapper.sort

# Public module methods.
def app(appId, **kwargs):
    keys = ['appId', 'lang', 'country']
    output = _wrapper._execute_api('app', keys, **{'appId': appId, **kwargs})
    return output


def list(**kwargs):
    keys = [
        'collection', 'category', 'age', 'num',
        'lang', 'country', 'fullDetail'
    ]
    output = _wrapper._execute_api('list', keys, **kwargs)
    return output


def search(term, **kwargs):
    keys = [
        'term', 'num', 'lang',
        'country', 'fullDetail', 'price'
    ]
    output = _wrapper._execute_api('search', keys,  **{'term': term, **kwargs})
    return output


def developer(devId, **kwargs):
    keys = ['devId', 'lang', 'country', 'num', 'fullDetail']
    output = _wrapper._execute_api(
        'developer', keys,  **{'devId': devId, **kwargs})
    return output


def suggest(term, **kwargs):
    keys = ['term', 'lang', 'country']
    output = _wrapper._execute_api(
        'suggest', keys,  **{'term': term, **kwargs})
    return output


def reviews(appId, **kwargs):
    keys = [
        'appId', 'lang', 'country', 'sort',
        'num', 'paginate', 'nextPaginationToken'
    ]
    output = _wrapper._execute_api(
        'reviews', keys,  **{'appId': appId, **kwargs})
    return output


def similar(appId, **kwargs):
    keys = ['appId', 'lang', 'country', 'fullDetail']
    output = _wrapper._execute_api(
        'similar', keys,  **{'appId': appId, **kwargs})
    return output


def permissions(appId, **kwargs):
    keys = ['appId', 'lang', 'short']
    output = _wrapper._execute_api(
        'permissions', keys,  **{'appId': appId, **kwargs})
    return output


def categories(**kwargs):
    output = _wrapper._execute_api('categories', [],  **kwargs)
    return output
