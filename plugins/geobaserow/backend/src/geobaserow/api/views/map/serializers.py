from geobaserow.views.models import MapViewFieldOptions
from rest_framework import serializers


class MapViewFieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapViewFieldOptions
        fields = ("hidden", "order")
