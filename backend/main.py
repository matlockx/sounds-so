from collections import namedtuple
import os
import random

import bottle
from first import first
import requests


# http://www.freesound.org/apiv2/search/text/?query=tiger&filter=duration:[3%20TO%2010]&fields=previews,images,license

SearchResult = namedtuple("SearchResult", ["id", "name", "tags", "desc", "url", "image"])
SlackResult = namedtuple("SlackResult", ["text"])

FREESOUND_API_TOKEN = os.getenv("FREESOUND_API_TOKEN")
assert FREESOUND_API_TOKEN

SLACK_TEAM_TOKEN = os.getenv("SLACK_TEAM_TOKEN")

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
        "fields": "id,name,tags,description,previews,images,license",
        "token": FREESOUND_API_TOKEN
    })

    for result in response.json()['results']:
        id = result['id']
        name = result['name']
        tags = result['tags']
        desc = result['description']
        url = result['previews']['preview-hq-mp3']
        image = result['images']['waveform_l']
        yield SearchResult(id, name, tags, desc, url, image)


def _sounds_like(term):
    response = list(freesound_search(term))
    random.shuffle(response)
    return response


# noinspection PyProtectedMember
@bottle.get("/api/v1/random/sound")
def sounds_like():
    bottle.response.set_header("Access-Control-Allow-Origin", "*")

    sounds = _sounds_like(bottle.request.params.get('like', ''))
    return first(r._asdict() for r in sounds) or {}


# noinspection PyProtectedMember
@bottle.post("/api/v1/slack/webhook")
def sounds_like():
    token = bottle.request.forms['token']
    if token != SLACK_TEAM_TOKEN:
        bottle.abort(403, "slack token invalid")

    trigger_word = bottle.request.forms['trigger_word']
    text = bottle.request.forms['text']
    term = text.replace(trigger_word, "")

    sounds = _sounds_like(term)
    response = first(r._asdict() for r in sounds) or None

    if response:
        return SlackResult(response['url'])._asdict()
    else:
        return SlackResult("")._asdict()


@bottle.get("/api/v1/random/sound/redirect")
def sounds_like_redirect():
    response = _sounds_like(bottle.request.params.get('like', ''))
    bottle.redirect(first(r.url for r in response) or bottle.abort(404))
