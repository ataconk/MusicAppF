from django import forms


class ArtistForm(forms.Form):
    artistName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter an artist name'}))