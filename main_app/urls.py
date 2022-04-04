from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('artists/', views.search_by_artist, name="search_by_artist"),
    path('artists/<str:artist_id>/', views.artist_detail, name="artist_detail"),

    path('albums/', views.search_by_album, name="search_by_album"),
    path('albums/<str:album_id>/', views.album_detail, name="album_detail"),

    path('mycollection/', views.view_collection, name="view_collection")


]
