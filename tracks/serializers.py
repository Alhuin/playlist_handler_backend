from rest_framework import serializers

from tracks.models import Artist, ArtistLink, Track, TrackLink


class ArtistLinkSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = ArtistLink
        fields = "__all__"


class TrackLinkSerializer(serializers.ModelSerializer):
    track = serializers.SlugRelatedField(slug_field="artists_and_title", read_only=True)

    class Meta:
        model = TrackLink
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Track
        fields = "__all__"
