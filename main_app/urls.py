from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('accounts/signup/', views.signup, name="signup"),

    path('artists/', views.search_by_artist, name="search_by_artist"),
    path('artists/<str:artist_id>/', views.artist_detail, name="artist_detail"),

    path('albums/', views.search_by_album, name="search_by_album"),
    path('albums/<str:album_id>/', views.album_detail, name="album_detail"),
    path('albums/<str:album_id>/add', views.add_to_collection, name="add_to_collection"),
    path('albums/<str:album_id>/remove', views.remove_from_collection, name="remove_from_collection"),

    path('mycollection/', views.view_collection, name="view_collection")


]
