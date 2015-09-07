from collections import namedtuple
import os
import random
import functools
import bottle
from first import first
import requests

SearchResult = namedtuple("SearchResult", ["id", "name", "tags", "desc", "url", "image"])
SlackResult = namedtuple("SlackResult", ["text", "channel"])

FREESOUND_API_TOKEN = os.getenv("FREESOUND_API_TOKEN")
SLACK_TEAM_TOKEN = os.getenv("SLACK_TEAM_TOKEN")
SLACK_INCOMING_WEBHOOK_URL = os.getenv("SLACK_INCOMING_WEBHOOK_URL")

assert FREESOUND_API_TOKEN
assert SLACK_TEAM_TOKEN
assert SLACK_INCOMING_WEBHOOK_URL

FREESOUND_SEARCH_ENDPOINT = "http://www.freesound.org/apiv2/search/text/"
SOUNDCLOUD_ENDPOINT = "http://api.soundcloud.com/tracks"


def shuffled(values):
    values = list(values)
    random.shuffle(values)
    return values


@functools.lru_cache()
def soundcloud_search(term):
    response = requests.get(SOUNDCLOUD_ENDPOINT, params={
        "q": term
    })

    result = []
    for result in response.json():
        id = result['id']
        name = result['title']
        tags = result['tag_list']
        desc = result['description']
        url = result['permalink_url']
        image = result['waveform_url']
        result.append(SearchResult(id, name, tags, desc, url, image))

    return result


@functools.lru_cache()
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

    result = []
    for result in response.json()['results']:
        id = result['id']
        name = result['name']
        tags = result['tags']
        desc = result['description']
        url = result['previews']['preview-hq-mp3']
        image = result['images']['waveform_l']
        result.append(SearchResult(id, name, tags, desc, url, image))

    return result


# noinspection PyProtectedMember
@bottle.get("/api/v1/random/sound")
def sounds_like():
    sounds = shuffled(freesound_search(bottle.request.params.get('like', '')))
    return first(r._asdict() for r in sounds) or {}


# noinspection PyProtectedMember
@bottle.post("/api/v1/slack/webhook")
def sounds_like():
    token = bottle.request.forms['token']
    if token != SLACK_TEAM_TOKEN:
        bottle.abort(403, "slack token invalid {}".format(token))

    term = bottle.request.forms['text']

    channel = bottle.request.forms['channel_id']
    freesounds = first(shuffled(freesound_search(term)))
    soundcloud = first(shuffled(soundcloud_search(term)))

    if freesounds or soundcloud:
        slack_response = {
            "text": soundcloud.url if soundcloud else freesounds.url,
            "channel": channel,
            "unfurl_links": True,
            "unfurl_media": True,
            "attachments": [
                {
                    "title": "From freesound.org",
                    "fields": [
                        {
                            "title": freesounds.name,
                            "value": freesounds.url,
                            "short": True
                        }
                    ],
                    "color": "#7CD197"
                }
            ] if freesounds else []
        }

        requests.post(SLACK_INCOMING_WEBHOOK_URL, json=slack_response)
        return
    else:
        return "No audio found"


@bottle.get("/api/v1/random/sound/redirect")
def sounds_like_redirect():
    response = shuffled(freesound_search(bottle.request.params.get('like', '')))
    bottle.redirect(first(r.url for r in response) or bottle.abort(404))
