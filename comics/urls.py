from django.urls import path

from comics.views import ChapterView, RetriveComicView, ComicListView

# from .views import GetCatalogAsura

urlpatterns = [
    path('comic-page/<int:pk>/', RetriveComicView.as_view()),
    path('comics/', ComicListView.as_view()),
    path('chapter/<int:pk>', ChapterView.as_view()),
]
