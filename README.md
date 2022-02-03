# google-play-scraper-py

[![PyPI](https://img.shields.io/pypi/v/google-play-scraper-py)](https://pypi.org/project/google-play-scraper-py/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/google-play-scraper-py)](https://github.com/blues-lab/google-play-scraper-py)
[![PyPI - License](https://img.shields.io/pypi/l/google-play-scraper-py)](https://github.com/blues-lab/google-play-scraper-py/blob/master/LICENSE)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/google-play-scraper-py)](https://github.com/blues-lab/google-play-scraper-py)

Python wrapper around the [Node.js module](https://github.com/facundoolano/google-play-scraper) to scrape application data from the Google Play store. Please refer to the module's page for the most up-to-date information about the API.

Any questions, suggestions, or issues with the underlying Node.js functionality should be directed to [facundoolano](https://github.com/facundoolano), who is the developer of the original module.

## Installation

First, ensure that you have the latest version of [Node.js](https://nodejs.org/en/download/) installed on your machine.

Then, install the library:

```
pip install google-play-scraper-py
```

This will also include the required Node dependencies.

## Example

```python
import scraper

result = scraper.app(appId='com.google.android.apps.translate')
print(result)
```

Results:

```python
{
  'adSupported': False,
  'androidVersion': 'VARY',
  'androidVersionText': 'Varies with device',
  'appId': 'com.google.android.apps.translate',
  'comments': [...],
  'contentRating': 'Everyone',
  'currency': 'USD',
  'description': ...,
  'descriptionHTML': ...,
  'developer': 'Google LLC',
  'developerAddress': '1600 Amphitheatre Parkway, Mountain View 94043',
  'developerEmail': 'translate-mobile-support@google.com',
  'developerId': '5700313618786177705',
  'developerInternalID': '5700313618786177705',
  'developerWebsite': 'http://support.google.com/translate',
  'editorsChoice': False,
  'free': True,
  'genre': 'Tools',
  'genreId': 'TOOLS',
  'headerImage': 'https://play-lh.googleusercontent.com/e4Sfy0cOmqpike76V6N6n-tDVbtbmt6MxbnbkKBZ_7hPHZRfsCeZhMBZK8eFDoDa1Vf-',
  'histogram': {'1': 458414,
               '2': 158469,
               '3': 420198,
               '4': 941431,
               '5': 5851958},
  'icon': 'https://play-lh.googleusercontent.com/ZrNeuKthBirZN7rrXPN1JmUbaG8ICy3kZSHt-WgSnREsJzo2txzCzjIoChlevMIQEA',
  'installs': '1,000,000,000+',
  'maxInstalls': 1004629541,
  'minInstalls': 1000000000,
  'offersIAP': False,
  'price': 0,
  'priceText': 'Free',
  'privacyPolicy': 'http://www.google.com/policies/privacy/',
  'ratings': 7830472,
  'recentChanges': 'Bug fixes and improvements',
  'reviews': 1924772,
  'score': 4.477567,
  'scoreText': '4.5',
  'screenshots': [...],
  'size': 'Varies with device',
  'summary': 'The world is closer than ever with over 100 languages',
  'title': 'Google Translate',
  'updated': 1616099487000,
  'url': 'https://play.google.com/store/apps/details?id=com.google.android.apps.translate&hl=en&gl=us',
  'version': 'Varies with device'
}
```

## Usage
Available methods:
- [app](#app): Retrieves the full detail of an application.
- [list](#list): Retrieves a list of applications from one of the collections at Google Play.
- [search](#search): Retrieves a list of apps that results of searching by the given term.
- [developer](#developer): Returns the list of applications by the given developer name.
- [suggest](#suggest): Given a string returns up to five suggestion to complete a search query term.
- [reviews](#reviews): Retrieves a page of reviews for a specific application.
- [similar](#similar): Returns a list of similar apps to the one specified.
- [permissions](#permissions): Returns the list of permissions an app has access to.
- [categories](#categories): Retrieve a full list of categories present from dropdown menu on Google Play.

### app

Retrieves the full detail of an application. Options:

* `appId`: the Google Play id of the application (the `?id=` parameter on the url).
* `lang` (optional, defaults to `'en'`): the two letter language code in which to fetch the app page.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the applications. Needed when the app is available only in some countries.

### list
Retrieve a list of applications from one of the collections at Google Play. Options:

* `collection` (optional, defaults to `collection.TOP_FREE`): the Google Play collection that will be retrieved. Available options can bee found [here](https://github.com/facundoolano/google-play-scraper/blob/dev/lib/constants.js#L58).
* `category` (optional, defaults to no category): the app category to filter by. Available options can bee found [here](https://github.com/facundoolano/google-play-scraper/blob/dev/lib/constants.js#L3).
* `age` (optional, defaults to no age filter): the age range to filter the apps (only for FAMILY and its subcategories). Available options are `age.FIVE_UNDER`, `age.SIX_EIGHT`, `age.NINE_UP`.
* `num` (optional, defaults to 500): the amount of apps to retrieve.
* `lang` (optional, defaults to `'en'`): the two letter language code used to retrieve the applications.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the applications.
* `fullDetail` (optional, defaults to `false`): if `true`, an extra request will be made for every resulting app to fetch its full detail.


### search
Retrieves a list of apps that results of searching by the given term. Options:

* `term`: the term to search by.
* `num` (optional, defaults to 20, max is 250): the amount of apps to retrieve.
* `lang` (optional, defaults to `'en'`): the two letter language code used to retrieve the applications.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the applications.
* `fullDetail` (optional, defaults to `false`): if `true`, an extra request will be made for every resulting app to fetch its full detail.
* `price` (optional, defaults to `all`): allows to control if the results apps are free, paid or both.
    * `all`: Free and paid
    * `free`: Free apps only
    * `paid`: Paid apps only


### developer
Returns the list of applications by the given developer name. Options:

* `devId`: the name of the developer.
* `lang` (optional, defaults to `'en'`): the two letter language code in which to fetch the app list.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the applications. Needed when the app is available only in some countries.
* `num` (optional, defaults to 60): the amount of apps to retrieve.
* `fullDetail` (optional, defaults to `false`): if `true`, an extra request will be made for every resulting app to fetch its full detail.

### suggest
Given a string returns up to five suggestion to complete a search query term. Options:

* `term`: the term to get suggestions for.
* `lang` (optional, defaults to `'en'`): the two letter language code used to retrieve the suggestions.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the suggestions.

### reviews
Retrieves a page of reviews for a specific application.

Note that this method returns reviews in a specific language (english by default), so you need to try different languages to get more reviews. Also, the counter displayed in the Google Play page refers to the total number of 1-5 stars ratings the application has, not the written reviews count. So if the app has 100k ratings, don't expect to get 100k reviews by using this method.

You can get all reviews at once, by sending the `num` parameter (i.g. 5000), or paginated reviews (with 150 per page), by setting the `pagination` parameter to true;

You'll have to choose wich method is better for your use case.

By setting `num` + `paginate`, the num parameter will be ignored and you will receive a paginated response instead.

Options:

* `appId`: Unique application id for Google Play. (e.g. id=com.mojang.minecraftpe maps to Minecraft: Pocket Edition game).
* `lang` (optional, defaults to `'en'`): the two letter language code in which to fetch the reviews.
* `country` (optional, defaults to `'us'`): the two letter country code in which to fetch the reviews.
* `sort` (optional, defaults to `sort.NEWEST`): The way the reviews are going to be sorted. Accepted values are: `sort.NEWEST`, `sort.RATING` and `sort.HELPFULNESS`.
* `num` (optional, defaults to `100`): Quantity of reviews to be captured.
* `paginate` (optional, defaults to `false`): Defines if the result will be paginated
* `nextPaginationToken` (optional, defaults to `null`): The next token to paginate

### similar
Returns a list of similar apps to the one specified. Options:

* `appId`: the Google Play id of the application to get similar apps for.
* `lang` (optional, defaults to `'en'`): the two letter language code used to retrieve the applications.
* `country` (optional, defaults to `'us'`): the two letter country code used to retrieve the applications.
* `fullDetail` (optional, defaults to `false`): if `true`, an extra request will be made for every resulting app to fetch its full detail.

### permissions
Returns the list of permissions an app has access to.

* `appId`: the Google Play id of the application to get permissions for.
* `lang` (optional, defaults to `'en'`): the two letter language code in which to fetch the permissions.
* `short` (optional, defaults to `false`): if `true`, the permission names will be returned instead of
permission/description objects.


### categories
Retrieve a full list of categories present from dropdown menu on Google Play.

* this method has no options

## Throttling

All methods on the scraper have to access the Google Play server in one
form or another. When making too many requests in a short period of time
(specially when using the `fullDetail` option), is common to hit Google Play's
throttling limit. That means requests start getting status 503 responses with
a captcha to verify if the requesting entity is a human (which is not :P).
In those cases the requesting IP can be banned from making further requests for a
while (usually around an hour).

To avoid this situation, all methods now support a `throttle` property, which
defines an upper bound to the amount of requests that will be attempted per second.
Once that limit is reached, further requests will be held until the second passes.

```js
import scraper

scraper.search(term='panda', throttle=10)
```

By default, no throttling is applied.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
