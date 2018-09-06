# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup


headers = {'Authorization': 'Bearer 7gZx9fzK7jlYr8H79vTGnadYuevPD8bqrmczseBehQCtE2L0Iahc54cWeB2NbwWX'}
base_url = "http://api.genius.com"



#############


def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()

    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)

    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text()
    lyrics = lyrics.replace('\n', ' ')

    return lyrics


###############


#if __name__ == "__main__":

def getLyrics(song_title, artist_name):
    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
        else:
            song_info = None

    if song_info is not None:
        song_api_path = song_info["result"]["api_path"]
        final = lyrics_from_song_api_path(song_api_path)

        for ch in ['...','..','.',',','!','?']:
            if ch in final:
                final = final.replace(ch," ")
        wordList = final.lower().split()
        return wordList
    else:
        return False

#song_title = "Öp"
#artist_name = "Tarkan"
#print(getLyrics(song_title, artist_name))


