from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=50)
    artists = models.ManyToManyField(Artist)
    release_date = models.DateTimeField("release date")
    image = models.URLField(max_length=200)

    @property
    def artists_and_title(self):
        return f"{', '.join([artist.name for artist in self.artists.all()])} - {self.title}"

    def __str__(self) -> str:
        return self.artists_and_title


class Link(models.Model):
    service = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    class Meta:
        abstract = True
        default_related_name = "link_set"


class TrackLink(Link):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{' ,'.join([a.name for a in self.track.artists.all()])} - {self.track.title} <{self.service}>"


class ArtistLink(Link):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.artist.name} <{self.service}>"
