from collections import namedtuple
import random
import bottle
import requests
import json
from attrdict import AttrDict as attrdict

# http://www.freesound.org/apiv2/search/text/?query=tiger&filter=duration:[3%20TO%2010]&fields=previews,images,license

SearchResult = namedtuple("SearchResult", ["url", "image"])

with open('freesound_credentials.json') as fp:
    FREESOUND_CREDENTIALS = attrdict(json.load(fp))

FREESOUND_SEARCH_ENDPOINT = "http://www.freesound.org/apiv2/search/text/"

def freesound_search(term):
    """Queries freesound.org by using the following filter criteria by default:
        - license: free
        - duration from 3 to 10 seconds
        - and the given term

        Search: http://www.freesound.org/docs/api/resources_apiv2.html#search-resources
        Response: http://www.freesound.org/docs/api/resources_apiv2.html#sound-instance-response
    """
    response = requests.get(FREESOUND_SEARCH_ENDPOINT, params={
        "query": term,
        "filter": 'duration:[3 TO 10] license:"Creative Commons 0"',
        "fields": "previews,images,license",
        "token": FREESOUND_CREDENTIALS.secret
    })

    for result in response.json()['results']:
        url = result['previews']['preview-hq-mp3']
        image = result['images']['waveform_l']
        yield SearchResult(url, image)


@bottle.get("/api/v1/random/sound")
def sounds_like():
    bottle.response.set_header("Access-Control-Allow-Origin", "*")

    response = tuple(freesound_search("tiger"))
    if not response:
        return {}
    else:
        # noinspection PyProtectedMember
        return random.choice(response)._asdict()
