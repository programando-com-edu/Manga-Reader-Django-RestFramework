from django.urls import path

from comics.views import ChapterImages, RetriveComicView, ComicListView

# from .views import GetCatalogAsura

urlpatterns = [
    path('comic-page/<int:pk>/', RetriveComicView.as_view()),
    path('comics/', ComicListView.as_view()),
    path('chapter/<int:pk>', ChapterImages.as_view()),
]
