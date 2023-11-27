from django.urls import path
from .views import GetCatalogAsura

urlpatterns = [
    path('get-catalog-asura/', GetCatalogAsura.as_view()),
]
