from django.contrib import admin

from tracks.models import Artist, ArtistLink, Track, TrackLink


admin.site.register(Track)
admin.site.register(TrackLink)
admin.site.register(Artist)
admin.site.register(ArtistLink)
