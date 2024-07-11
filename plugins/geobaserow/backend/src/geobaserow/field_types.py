import json

from baserow.contrib.database.fields.registries import FieldType
from baserow.contrib.database.formula import BaserowFormulaTextType
from baserow.contrib.database.table.models import GeneratedTableModel
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

from .models import PointField
from .serializers import GeometryPointFieldSerializerField


class PointFieldType(FieldType):
    type = "point"
    model_class = PointField
    allowed_fields = []
    serializer_field_names = []

    def get_serializer_field(self, instance, **kwargs):
        required = kwargs.get("required", False)
        return GeometryPointFieldSerializerField(
            **{
                "required": required,
                "allow_null": not required,
                **kwargs,
            }
        )

    def get_internal_value_from_db(self, row: "GeneratedTableModel", field_name: str):
        geo = getattr(row, f"{field_name}")
        if not geo:
            return None
        else:
            return geo.wkt

    def prepare_value_for_db(self, instance, value):
        if value is None:
            return value

        value = {"type": "Point", "coordinates": [value["lng"], value["lat"]]}
        value = json.dumps(value)
        return GEOSGeometry(value)

    def get_model_field(self, instance, **kwargs):
        return models.PointField(blank=True, null=True, srid=4326, **kwargs)

    def random_value(self, instance, fake, cache):
        return fake.name()

    def to_baserow_formula_type(self, field):
        return BaserowFormulaTextType()

    def from_baserow_formula_type(self, formula_type):
        return PointField()
