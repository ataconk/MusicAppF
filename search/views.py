from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from jpype import *
from .forms import ArtistForm
from .spotifyAPI import find_artist, get_albums, show_album_tracks, createZemberek, get_album


def index(request):
    if request.method == "POST":
        artistForm = ArtistForm(request.POST)
        if artistForm.is_valid():
            artist = find_artist(artistForm.cleaned_data)
            albums = get_albums(artist)
            template = 'search/templates/search/index.html'
            context = {
                'form': artistForm,
                'artist': artist,
                'albums': albums,
                'albums_display': "block"
            }
            return render(request, template, context)
    else:
        artistForm = ArtistForm()
        template = 'search/templates/search/index.html'
        context = {
            'form': artistForm,
            'albums_display': "none"

        }
        return render(request, template, context)


def analysis(request):
    template = 'search/templates/search/analysis.html'
    album_id = request.GET.get('q', '')
    zemberek = createZemberek()
    album_info = show_album_tracks(album_id, zemberek)
    album = get_album(album_id)
    numOfSongsInAlbum = len(album_info["data"])
    shutdownJVM()
    context = {
        "album_id": album_id,
        "album_info": album_info,
        "numOfSongs": numOfSongsInAlbum,
        "album": album
    }
    return render(request, template, context)







