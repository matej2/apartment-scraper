from rest_framework import serializers
from .models import Apartment


class ApartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Apartment
        fields = ('url', 'title', 'rent')