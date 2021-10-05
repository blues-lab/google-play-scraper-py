import scraper.wrapper as _wrapper
import scraper.exceptions as _exceptions

# Public module attribues.
collection = _wrapper.collection
category = _wrapper.category
age = _wrapper.age
sort = _wrapper.sort

# Public module methods - wrappers around the original API.
def app(appId, lang='en', country='us', **kwargs):
    """
    Retrieves the full detail of an application.

    Parameters
    ----------
    appId : str
        The Google Play id of the application (the ?id= parameter on the url).
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    dict
        Dictionary containing the full details of an application.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'appId': appId,
        'lang': lang,
        'country': country,
        **kwargs
    }
    return _wrapper.app(**vargs)

def list(collection=None, category=None, age=None, num=500, lang='en', country='us', fullDetail=False, **kwargs):
    """
    Retrieves a list of applications from one of the collections at Google Play.

    Parameters
    ----------
    collection : str, optional
        The Google Play collection that will be retrieved (default is scraper.collection['TOP_FREE'])
    category : str, optional
        The app category to filter by (default is None).
    age : {None, scraper.age['FIVE_UNDER'], scraper.age['SIX_EIGHT'], scraper.age['NINE_UP']}, optional
        The age range to filter the apps (only for FAMILY and its subcategories; default is None).
    num : int, optional
        The number of apps to retrieve (default is 500).
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    fullDetail : bool, optional
        If True, an extra request will be made for every resulting app to fetch its full detail (default is False).
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict
        List of dictionaries containing details of applications from one of the collections at Google Play.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'collection': _wrapper.collection['TOP_FREE'] if collection is None else collection,
        'category': category,
        'age': age,
        'num': num,
        'lang': lang,
        'country': country,
        'fullDetail': fullDetail,
        **kwargs
    }
    return _wrapper.list(**vargs)

def search(term, num=20, lang='en', country='us', fullDetail=False, price='all', **kwargs):
    """
    Retrieves a list of apps that results from searching by the given term.

    Parameters
    ----------
    term : str
        The term to search by.
    num : int, optional
        The number of apps to retrieve (default is 20, max is 250).
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    fullDetail : bool, optional
        If True, an extra request will be made for every resulting app to fetch its full detail (default is False).
    price : {'all', 'free', 'paid'}, optional
        Allows to control if the results apps are free, paid or both (default is 'all').
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict
        List of dictionaries containing details of applications that result from searching by the given term.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'term': term,
        'num': num,
        'lang': lang,
        'country': country,
        'fullDetail': fullDetail,
        'price': price,
        **kwargs
    }
    return _wrapper.search(**vargs)

def developer(devId, lang='en', country='us', num=60, fullDetail=False, **kwargs):
    """
    Returns the list of applications by the given developer name.

    Parameters
    ----------
    devId : str
        The name of the developer.
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    num : int, optional
        The number of apps to retrieve (default is 60).
    fullDetail : bool, optional
        If True, an extra request will be made for every resulting app to fetch its full detail (default is False).
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict
        List of dictionaries containing details of applications by the given developer name.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'devId': devId,
        'lang': lang,
        'country': country,
        'num': num,
        'fullDetail': fullDetail,
        **kwargs
    }
    return _wrapper.developer(**vargs)

def suggest(term, lang='en', country='us', **kwargs):
    """
    Given a string returns up to five suggestion to complete a search query term.

    Parameters
    ----------
    term : str
        The term to get suggestions for.
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of str
        List of suggestions to complete the given search query term.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'term': term,
        'lang': lang,
        'country': country,
        **kwargs
    }
    return _wrapper.suggest(**vargs)

def reviews(appId, lang='en', country='us', sort=None, num=100, paginate=False, nextPaginationToken=None, **kwargs):
    """
    Retrieves a page of reviews for a specific application.

    Parameters
    ----------
    appId : str
        The Google Play id of the application (the ?id= parameter on the url).
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    sort : {scraper.sort['NEWEST'], scraper.sort['RATING'], scraper.sort['HELPFULNESS']}, optional
        The way the reviews are going to be sorted (default is scraper.sort['NEWEST']).
    num : int, optional
        Number of reviews to be captured (default is 100).
    paginate : bool, optional
        Defines if the result will be paginated (default is False).
    nextPaginationToken : str
        The next token to paginate (default is None).
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict
        List of dictionaries containing the reviews and the nextPaginationToken.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'appId': appId,
        'lang': lang,
        'country': country,
        'sort': _wrapper.sort['NEWEST'] if sort is None else sort,
        'num': num,
        'paginate': paginate,
        'nextPaginationToken': nextPaginationToken,
        **kwargs
    }
    return _wrapper.reviews(**vargs)

def similar(appId, lang='en', country='us', fullDetail=False, **kwargs):
    """
    Returns a list of similar apps to the one specified.

    Parameters
    ----------
    appId : str
        The Google Play id of the application to get similar apps for.
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    country : str, optional
        The two letter country code used to retrieve the applications (default is 'us').
    fullDetail : bool, optional
        If True, an extra request will be made for every resulting app to fetch its full detail (default is False).
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict
        List of dictionaries containing details of applications similar to the one specified.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'appId': appId,
        'lang': lang,
        'country': country,
        'fullDetail': fullDetail,
        **kwargs
    }
    return _wrapper.similar(**vargs)

def permissions(appId, lang='en', short=False, **kwargs):
    """
    Returns the list of permissions an app has access to.

    Parameters
    ----------
    appId : str
        The Google Play id of the application to get permissions for.
    lang : str, optional
        The two letter language code in which to fetch the app page (default is 'en').
    short : str, optional
        If True, the permission names will be returned instead of permission/description objects (default is False).
    throttle : int, optional
        Upper bound to the amount of requests that will be attempted per second (default is None).
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of dict or list of str
        List of dictionaries (if `short` is True) or list of strings (if `short` is False)
        corresponding to the permissions an app has access to.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    vargs = {
        'appId': appId,
        'lang': lang,
        'short': short,
        **kwargs
    }
    return _wrapper.permissions(**vargs)

def categories(**kwargs):
    """
    Retrieve a full list of categories present from dropdown menu on Google Play Store.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    list of str
        List containing available categories from the dropdown menu on Google Play Store.

    Raises
    ------
    ScraperException
        Raised if an error occured when scraping Google Play Store or parsing the response.
    """
    return _wrapper.categories(**kwargs)
