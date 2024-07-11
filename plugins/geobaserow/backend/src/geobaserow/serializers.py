import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.fields import empty
from rest_framework_gis.serializers import GeometryField


class GeometryPointFieldSerializerField(GeometryField):
    def to_internal_value(self, value):
        value = {
            "type": "Point",
            "coordinates": [value['lng'], value['lat']]
        }
        value = json.dumps(value)
        return GEOSGeometry(value)

    def to_representation(self, value):
        return value.wkt

    def run_validation(self, data=empty):
        """
        Here we override rest_framework run_validation as it gives json encoding errors with baserow which uses
        serializer.validated_data in row patch view, rather that serializer.data.
        Here we force to return the json representation to bypass the error
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data
        value = self.to_internal_value(data)
        self.run_validators(value)
        return self.to_representation(value)
