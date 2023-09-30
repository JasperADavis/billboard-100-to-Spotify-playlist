import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

limit_by_date = False
create_playlist = True

# SPOTIPY API CREDENTIALS
SPOTIPY_CLIENT_ID = "" # Replace with Spotipy credentials
SPOTIPY_CLIENT_SECRET = "" # Replace with Spotipy credentials
redirect_uri = "http://example.com"
scope = "user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri="http://example.com"))

user_id = sp.current_user()["id"]

current_playlists = sp.current_user_playlists()


playlist_names = []
for playlist in current_playlists["items"]:
    playlist_names.append(playlist["name"])



# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])



date_selection = input("What time period? (YYYY-MM-DD)\n")
# date_selection = "1994-09-23"

year = date_selection[:4]
playlist_name = f"{date_selection} Billboard 100"
if playlist_name in playlist_names:
    print("Playlist by that name already exists!")
    create_playlist = False

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_selection}/")
website_html = response.text


soup = BeautifulSoup(website_html, "html.parser")
article_text = (soup.select(".a-no-trucate" ))
# article_text = (soup.find_all("h3", id="title-of-a-story"))


music_list = [(article.text).strip() for article in article_text]

songs_only = music_list[::2]
artists_only = music_list[1::2]

song_uri_list = []

if create_playlist:
    for i in range(len(songs_only)):
        song = songs_only[i]
        artist = artists_only[i]
        if limit_by_date:
            result = sp.search(q=f'{song} by {artist} year:{int(year) - 38}-{year}', type="track", limit=1)
        else:
            result = sp.search(q=f'{song} by {artist}', type="track", limit=1)

        try:
            song_uri_list.append(result["tracks"]["items"][0]["external_urls"]["spotify"])
        except:
            pass
        else:
            pass
        finally:
            pass
    playlist_creation = sp.user_playlist_create(user=user_id, name=playlist_name)
    playlist_id = playlist_creation["id"]

    sp.playlist_add_items(playlist_id=playlist_id, items=song_uri_list)

    print(f"Check out the new playlist here: \n{playlist_creation['external_urls']['spotify']}")
else:
    pass
