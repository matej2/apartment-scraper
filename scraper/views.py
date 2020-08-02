from __future__ import print_function

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view

from scraper.models import Apartment
from .common import main
from .serializers import ApartmentSerializer


@api_view(['GET'])
def run_all(request):
    status = main(request)
    return JsonResponse({
        'success': status
    }, status=200)


class ProductRESTView(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
