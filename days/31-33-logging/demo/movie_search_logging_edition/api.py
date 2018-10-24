from typing import List

import logbook
import requests
import collections
import random

import time

Movie = collections.namedtuple('Movie', 'imdb_code, title, director, keywords, '
                                        'duration, genres, rating, year, imdb_score')

# log information as the application runs
api_log = logbook.Logger('API')

# given a string, search the the html of the talkpython movie search site
def find_movie_by_title(keyword: str) -> List[Movie]:
    # initialize an object to keep track the run time
    t0 = time.time()

    api_log.trace('Starting search for {}'.format(keyword))

    # fail safe in case this function is not given a string object and report it into the logger object
    if not keyword or not keyword.strip():
        api_log.warn("No keyword supplied")
        raise ValueError('Must specify a search term.')

    # move search url, it's here because there's no point in generating it any sooner and it's only tailored to this website
    url = f'http://movie_service.talkpython.fm/api/search/{keyword}'

    # create requests object
    resp = requests.get(url)
    api_log.trace("Request finished, status code {}.".format(resp.status_code))
    resp.raise_for_status()

    # the site's html is designed in such a way that simply merging the base url with the searched word, it will return a set of results that can be formatted into json format
    # this is not universal as proven through web scraping experiences
    results = resp.json()
    # call on the create random error method
    results = create_random_errors(results)

    movies = []
    for r in results.get('hits'):
        movies.append(Movie(**r))

    t1 = time.time()

    api_log.trace('Finished search for {}, {:,} results in {} ms.'.format(
        keyword, len(movies), int(1000 * (t1 - t0))))

    return movies


def create_random_errors(results):
    # This is a method to occasionally create some more
    # interesting errors other than simply network connectivity errors
    # which are the only "real" errors. This will let us test
    # more types.

    num = random.randint(1, 20)
    if 16 < num <= 18:
        return {}  # Whoops! No data.
    elif 18 < num <= 20:
        raise StopIteration()

    return results  # no errors here.
