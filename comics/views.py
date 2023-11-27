from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .utils import AsuraCatalog

# Create your views here.


class GetCatalogAsura(APIView):
    def get(self, request, *args, **kwargs):
        AsuraCatalog()
        return Response('', status=status.HTTP_201_CREATED)
