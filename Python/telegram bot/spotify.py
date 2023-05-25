from base64 import b64encode
from requests import post, get
from json import loads
from random import sample

class SpotifyApi():

    CLIENT_ID = '1115343e4eb14e87b99ae953486657b2'
    CLIENT_SECRET = 'b13f6129750d49bdbfa5f559be4e0d56'
    URL_SPOTIFY_API = "https://api.spotify.com/v1/"

    def __init__(self):
        self.artist = None
        self.artist_id = None
        self.artist_name = None
        self.url_next_artist = None
        self.amount_artists = None
        self.track = None
        self.track_id = None
        self.track_name = None
        self.url_next_track = None
        self.amount_tracks = None

    def encode_client_credentials(self):
        """Возвращает строку в кодироквке base64"""
        auth_string = self.CLIENT_ID + ':' + self.CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(b64encode(auth_bytes), "utf-8")

        return auth_base64

    @property
    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + self.encode_client_credentials(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        request = post(url, headers=headers, data=data)
        json_result = loads(request.content)

        return json_result["access_token"]

    @property
    def get_auth_header(self):
        return {"Authorization": "Bearer " + self.get_token}

    def search(self, query):
        if query.startswith(self.URL_SPOTIFY_API):
            url = query
        else:
            url = self.URL_SPOTIFY_API + query
        headers = self.get_auth_header
        result = get(url, headers=headers)
        json_result = loads(result.content)
        return json_result

    def search_query(self, type, name):
        query = f"search?q={name}&type={type}&limit=1"
        return self.search(query)

    def search_artist(self, name):
        return self.refresh_artist(self.search_query("artist", name))

    def refresh_artist(self, json_result):
        answer = json_result["artists"]
        self.artist = answer['items'][0]
        self.artist_name = self.artist['name']
        self.artist_id = self.artist['id']
        self.url_next_artist = answer['next']

    @property
    def artist_data(self):
        data = {'name': self.artist['name'],
                'link': self.artist['external_urls']['spotify'],
                'images': self.artist['images'][1]['url'],
                'next': self.url_next_artist
                }
        return data

    def next_artist(self):
        self.refresh_artist(self.search(self.url_next_artist))
        return self.artist_data

    def search_track(self, name):
        return self.refresh_track(self.search_query("track", name))

    def refresh_track(self, json_result):
        answer = json_result["tracks"]
        self.track = answer['items'][0]
        self.track_id = self.track['id']
        self.track_name = self.track['name']
        self.url_next_track = answer['next']

    @property
    def track_data(self):
        data = {'artist': self.track['artists'][0]['name'],
                'name': self.track['name'],
                'images': self.track["album"]['images'][1]['url'],
                'link': self.track['external_urls']['spotify'],
                'preview_url': self.track['preview_url'],
                'next': self.url_next_track,
                }
        return data

    def next_track(self):
        self.refresh_track(self.search(self.url_next_track))
        return self.track_data

    def search_artist_and_track(self, artist_name, track_name):
        query = f'artist:{artist_name} track:{track_name}'
        result = self.search_query('track', query)['tracks']['items'][0]
        self.artist_id = result['artists'][0]['id']
        self.track_id = result['id']
        return {'artist': result['artists'][0]['name'],
                "track": result["name"],
                "album": result["album"]["name"],
                "release_date": result["album"]["release_date"][-2:] + result["album"]["release_date"][4:-2] + result["album"]["release_date"][:4],
                'id': result['id'],
                "preview_url": result["preview_url"],
                'link': result['external_urls']['spotify']
                }

    def related_artists(self):
        query = f'artists/{self.artist_id}/related-artists'
        result = self.search(query)['artists']
        related_name = {artist['name']: {'id': artist['id'],
                                         'link': artist['external_urls']['spotify']
                                         }
                        for artist in result}
        return sample(list(related_name.items()), 3)

    def related_track(self, track_name):
        self.artist_by_track(self.track_data['artist'])
        query = f'recommendations?&limit=3&seed_artists={self.artist_id}&seed_tracks={self.track_id}'
        result = self.search(query)['tracks']

        related = {track['name']: {'artist': track['artists'][0]['name'],
                                   'link': track['external_urls']['spotify']}
                   for track in result}
        return related

    def track_by_artist(self, track_name):
        return self.search_artist_and_track(self.artist_name, track_name)

    def artist_by_track(self, artist_name):
        return self.search_artist_and_track(artist_name, self.track_name)
