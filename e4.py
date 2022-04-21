""" Written by Anton Caceres
    https://github.com/MA3STR0/PythonAsyncWorkshop
"""

from urllib.request import urlopen
import time

__author__ = 'Anton Caceres'

URLS = [
    'http://dsl.sk',
    'http://stuba.sk',
    'http://shmu.sk',
    'http://root.cz',
]


def request_greetings():
    responses = []
    for url in URLS:
        resp = urlopen(url)
        responses.append(resp.read().decode('utf-8', errors='replace'))
    texts = '\n'.join(responses)
    return texts


if __name__ == "__main__":
    t1 = time.time()
    greetings = request_greetings()
    print(time.time() - t1, "seconds passed")
    print(greetings)
