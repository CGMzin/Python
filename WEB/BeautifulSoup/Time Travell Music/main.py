from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import requests, spotipy


scope = 'playlist-modify-private'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="3f6b7fd424304733bb1bb990ee06b566",
        client_secret="4aa8086cadb34465ab50437fbb499e24",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format 'YYYY MM DD': ").split()

response_vagalume = requests.get(f"https://www.vagalume.com.br/top100/musicas/geral/{date[0]}/{date[1]}/{date[2]}")
response_vagalume.encoding = 'UTF-8'
html = response_vagalume.text

soup = BeautifulSoup(html, "html.parser")
    
titles = [title.getText() for title in soup.find_all(name="a", class_="w1 h22")]

for title in titles:
    if title.find("(tra") != -1:
        titles[titles.index(title)] = title[:title.find("(tra")]
    if title.find("(Tra") != -1:
        titles[titles.index(title)] = title[:title.find("(Tra")]

song_uris = []

for song in titles:
    result = sp.search(q=f"track: {song} year: {date[0]}", type="track")
    try:
        song_uris.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"Mais tocadas - {date[0]}/{date[1]}/{date[2]}", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)