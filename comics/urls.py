from django.urls import path

from comics.views import RetriveComicView

# from .views import GetCatalogAsura

urlpatterns = [
    # path('get-catalog-asura/', GetCatalogAsura.as_view()),
    path('comic-page/<int:pk>', RetriveComicView.as_view()),
]
