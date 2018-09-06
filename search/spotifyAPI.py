import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
from .geniusScraper import getLyrics
from .zemberek import getFinalScore
from jpype import *

client_id = "bf29747258d64bf891277bda6c81c682"
client_secret = "3acd3751483148bb9e962d9e56bd9abb"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df_tracks = pd.DataFrame(columns=["Track Name", "Album", "Track ID", "Danceability", "Energy", "Arousal", "Valence",
                                  "Lyrics Score", "Positivity"])
i = 0
#
#

def createZemberek():
    if not isJVMStarted():
        startJVM(getDefaultJVMPath(), "-Djava.class.path=/Users/Tolga/Desktop/zemberek-tum-2.0.jar",
                 "-ea")  # JVM başlat
    Tr = JClass(
        "net.zemberek.tr.yapi.TurkiyeTurkcesi")  # Türkiye Türkçesine göre çözümlemek için gerekli sınıfı hazırla
    tr = Tr()  # tr nesnesini oluştur
    Zemberek = JClass("net.zemberek.erisim.Zemberek")  # Zemberek sınıfını yükle
    zemberek = Zemberek(tr)  # zemberek nesnesini oluştur
    return zemberek


def rescale(num):
    OldRange = (1 - 0)
    NewRange = (1 - (-1))
    NewValue = (((num - 0) * NewRange) / OldRange) + (-1)
    return NewValue


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def get_audio_features(track_id):
    features = sp.audio_features(track_id)
    danceability = float(json.dumps(features[0]["danceability"], indent=4))
    danceability = rescale(danceability)

    energy = float(json.dumps(features[0]["energy"], indent=4))
    energy = rescale(energy)

    valence = float(json.dumps(features[0]["valence"], indent=4))
    valence = rescale(valence)

    arousal = (danceability + energy) / 2
    features_temp = [danceability, energy, arousal, valence]
    return features_temp


def show_album_tracks(album_id, zemberek):
    tracks = []
    results = sp.album_tracks(album_id)
    result_album = sp.album(album_id)
    artist_name = json.dumps(result_album["artists"][0]["name"], ensure_ascii=False)
    artist_name = artist_name[1:-1]
    album_name = json.dumps(result_album["name"], ensure_ascii=False)
    album_name = album_name[1:-1]
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        global i
        track_index = i
        #print('  ', track['name'])
        #print('     ', track['id'])
        track_info = [track["name"], album_name, track["id"]]
        audio_features = get_audio_features(track["id"])

        song_title = track["name"]
        words = getLyrics(song_title, artist_name)
        if words:
            lyrics_score = [getFinalScore(words, zemberek)]
            valence = audio_features[-1]
            positivity = [(float(valence) + float(lyrics_score[0])) / 2]
            df_tracks.loc[track_index] = track_info + audio_features + lyrics_score + positivity
            i += 1
        else:
            lyrics_score = False
            lyrics_score = [0]
            valence = audio_features[-1]
            positivity = [float(valence) / 2]
            df_tracks.loc[track_index] = track_info + audio_features + lyrics_score + positivity
            i += 1

    return df_tracks.to_dict(orient="split")
#
# def show_artist_albums(artist, zemberek):
#     artist_name = artist["name"]
#     albums = []
#     results = sp.artist_albums(artist['id'], album_type='album')
#     albums.extend(results['items'])
#     while results['next']:
#         results = sp.next(results)
#         albums.extend(results['items'])
#     print('Total albums:', len(albums))
#     unique = set()  # skip duplicate albums
#     for album in albums:
#         name = album['name'].lower()
#         if "mix" not in name:
#             if not name in unique:
#                 print(name.title())
#                 #print()
#                 unique.add(name)
#                 #show_album_tracks(album, artist_name, zemberek)
#
def get_albums(artist):
    artist_name = artist["name"]
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    unique = {each["name"]: each for each in albums}.values()
    return unique

def get_album(album_id):
    album = sp.album(album_id)
    if album:
        return album
    else:
        return None

def find_artist(artist_input):
    artist = get_artist(artist_input["artistName"])
    if artist:
        return artist
    else:
        return False

#name = input("Enter an artist name: ")

# if artist:
#     album = get_albums(artist)
#
#     zemberek = createZemberek()
#     show_album_tracks(album, artist["name"], zemberek)
#     #show_artist_albums(artist, zemberek)
#     print(df_tracks.head())
#     shutdownJVM()
# else:
#     print("Can't find that artist")