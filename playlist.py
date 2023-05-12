from requests import get, post, delete
import math, random, re
import dotenv
import json

api_url = "https://api.spotify.com/v1"

def add_to_playlist(playlist_id : str, uris : list, position : int, header : json):
    playlist_endpoint = f'{api_url}/playlists/{playlist_id}/tracks'

    body = {
        'uris': [],
        'position': position
    }

    for uri in uris:
        body['uris'].append(f'spotify:track:{uri}')

    body = json.dumps(body)

    response = post(playlist_endpoint, headers=header, data=body)
    response_json = json.loads(response.content)

def remove_from_playlist(playlist_id : str, uris : list, header : json):
    playlist_endpoint = f'{api_url}/playlists/{playlist_id}/tracks'

    body = {
        'tracks': []
    }

    for uri in uris:
        body['tracks'].append({'uri':f'spotify:track:{uri}'})

    body = json.dumps(body)

    response = delete(playlist_endpoint, headers=header, data=body)
    response_json = json.loads(response.content)
    

'''
TODO
right now this only works for playlists of size exactly 20, so increase offset by total each iter, until total = 0
'''
def shuffler(playlist_id : str, header : json):
    total = 0
    while (offset := shuffle(playlist_id=playlist_id, offset=total, header=header)) > 0:
        total += offset
    


def shuffle(playlist_id : str, offset : int, header : json) -> int:
    playlist_endpoint = f'{api_url}/playlists/{playlist_id}/tracks'
    fields = f'?fields=limit%2Citems%28track%28name%2Curi%29%29&limit=20&offset={offset}'
    shuffler_endpoint = playlist_endpoint + fields

    response = get(shuffler_endpoint, headers=header)
    response_json = json.loads(response.content)

    limit = response_json['limit']
    tracks = response_json['items']

    uris = []
    for i in range(len(tracks)):
        uri = re.search(r'spotify:track:([^&]+)', tracks[i]['track']['uri'])
        uris.append(uri.group(1))
    uris_len = len(uris)

    remove_from_playlist(playlist_id=playlist_id, uris=uris, header=header)
    random.shuffle(uris)
    add_to_playlist(playlist_id=playlist_id, uris=uris, position=offset, header=header)

    return limit if uris_len > limit else uris_len
