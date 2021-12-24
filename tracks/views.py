from datetime import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views import generic
from rest_framework import permissions, viewsets

from tracks.models import Artist, ArtistLink, Track, TrackLink
from tracks.serializers import (
    ArtistLinkSerializer,
    ArtistSerializer,
    TrackLinkSerializer,
    TrackSerializer,
)


# API
class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tracks to be viewed or edited.
    """

    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artists to be viewed or edited.
    """

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArtistLinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows artist links to be viewed or edited.
    """

    queryset = ArtistLink.objects.all()
    serializer_class = ArtistLinkSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrackLinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows track links to be viewed or edited.
    """

    queryset = TrackLink.objects.all()
    serializer_class = TrackLinkSerializer
    permission_classes = [permissions.IsAuthenticated]


# App Views
class IndexView(generic.ListView):
    model = Track
    template_name = "tracks/index.html"
    context_object_name = "latest_tracks_list"


class TrackDetailView(generic.DetailView):
    model = Track
    template_name = "tracks/track_detail.html"


class ArtistDetailView(generic.DetailView):
    model = Artist
    template_name = "tracks/artist_detail.html"


def add(request):
    return render(request, "tracks/add.html")


def create(request):
    response = requests.post(
        "https://songwhip.com/api/songwhip/create",
        json={"url": request.POST["url"], "country": "FR"},
    )
    res = response.json()
    data = res["data"]

    if Track.objects.filter(
        title__exact=data["name"],
        release_date=datetime.strptime(data["releaseDate"], "%Y-%m-%dT%H:%M:%S.%fZ"),
    ).exists():
        return render(
            request,
            "tracks/add.html",
            {
                "error_message": "Track already exists.",
            },
        )

    track = Track(
        title=data["name"],
        release_date=make_aware(
            datetime.strptime(data["releaseDate"][:10], "%Y-%m-%d")
        ),
        image=data["image"],
    )

    track.save()

    for artist_data in data["artists"]:
        artist, created = Artist.objects.get_or_create(
            name=artist_data["name"],
            image=artist_data["image"],
        )
        if created:
            artist_links = {
                service: values[0]["link"]
                for service, values in artist_data["links"].items()
                if not values[0]["countries"] or "FR" in values[0]["countries"]
            }
            for service, url in artist_links.items():
                link = ArtistLink(artist=artist, service=service, url=url)
                link.save()

        track.artists.add(artist)

    track_links = {
        service: values[0]["link"]
        for service, values in data["links"].items()
        if not values[0]["countries"] or "FR" in values[0]["countries"]
    }

    for service, url in track_links.items():
        link = TrackLink(track=track, service=service, url=url)
        link.save()

    return HttpResponseRedirect(reverse("tracks:track_detail", args=(track.pk,)))
