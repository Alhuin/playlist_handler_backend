from django.urls import path

from tracks import views


app_name = "tracks"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add/", views.add, name="add"),
    path("track/<int:pk>/", views.TrackDetailView.as_view(), name="track_detail"),
    path("artist/<int:pk>/", views.ArtistDetailView.as_view(), name="artist_detail"),
    path("create/", views.create, name="create"),
]
