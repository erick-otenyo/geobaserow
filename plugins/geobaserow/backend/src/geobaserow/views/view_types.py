from baserow.contrib.database.api.fields.errors import (
    ERROR_FIELD_NOT_IN_TABLE,
    ERROR_INCOMPATIBLE_FIELD,
)
from baserow.contrib.database.fields.exceptions import (
    FieldNotInTable,
    IncompatibleField,
)
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.views.registries import ViewType
from django.db.models import Q
from django.urls import include, path
from geobaserow.api.views.map.serializers import MapViewFieldOptionsSerializer
from rest_framework.fields import empty
from rest_framework.serializers import PrimaryKeyRelatedField

from .models import (
    MapView,
    MapViewFieldOptions,
)


class CustomPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def run_validation(self, data=empty):
        """
        Here we override rest_framework run_validation as it gives j
        son encoding errors with baserow which uses
        serializer.validated_data in row patch view, rather that serializer.data.
        Here we force to return the json representation to bypass the error
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data
        value = self.to_internal_value(data)
        self.run_validators(value)

        return self.to_representation(value)


class MapViewType(ViewType):
    type = "map"
    model_class = MapView
    field_options_model_class = MapViewFieldOptions
    field_options_serializer_class = MapViewFieldOptionsSerializer
    allowed_fields = ["geo_field"]
    field_options_allowed_fields = ["hidden", "order"]
    serializer_field_names = ["geo_field"]
    serializer_field_overrides = {
        "geo_field": CustomPrimaryKeyRelatedField(
            queryset=Field.objects.all(),
            required=False,
            default=None,
            allow_null=True,
        ),
    }
    api_exceptions_map = {
        IncompatibleField: ERROR_INCOMPATIBLE_FIELD,
        FieldNotInTable: ERROR_FIELD_NOT_IN_TABLE,
    }
    can_decorate = True
    can_share = True
    has_public_info = True

    def get_api_urls(self):
        from geobaserow.api.views.map import urls as api_urls

        return [
            path("map/", include(api_urls, namespace=self.type)),
        ]

    def prepare_values(self, values, table, user):
        """
        Check if the provided geo field belongs to the same table.
        """

        geo_field_value = values.get("geo_field", None)
        if geo_field_value is not None:
            if isinstance(geo_field_value, int):
                values["geo_field"] = geo_field_value = Field.objects.get(
                    pk=geo_field_value
                )

            geo_field_value = geo_field_value.specific
            field_type = field_type_registry.get_by_model(geo_field_value)

            if not hasattr(field_type, "is_geo"):
                raise IncompatibleField()

            if not field_type.is_geo:
                raise IncompatibleField()

            if (
                    isinstance(geo_field_value, Field)
                    and geo_field_value.table_id != table.id
            ):
                raise FieldNotInTable(
                    "The provided geo field id does not belong to the map "
                    "view's table."
                )

        return super().prepare_values(values, table, user)

    def export_prepared_values(self, view):
        values = super().export_prepared_values(view)
        values["geo_field"] = view.geo_field_id
        return values

    def get_visible_field_options_in_order(self, map_view):
        return (
            map_view.get_field_options(create_if_missing=True)
            .filter(
                Q(hidden=False)
                # If the `geo_field_id` is set, we must always expose the field
                # because the values are needed.
                | Q(field_id=map_view.geo_field_id)
            )
            .order_by("order", "field__id")
        )

    def get_hidden_fields(self, view, field_ids_to_check=None, ):
        hidden_field_ids = set()
        fields = view.table.field_set.all()
        field_options = view.mapviewfieldoptions_set.all()

        if field_ids_to_check is not None:
            fields = [f for f in fields if f.id in field_ids_to_check]

        for field in fields:
            # If the `date_field_id` is set, we must always expose the field
            # because the values are needed.
            if field.id in [
                view.date_field_id,
            ]:
                continue

            field_option_matching = None
            for field_option in field_options:
                if field_option.field_id == field.id:
                    field_option_matching = field_option

            # A field is considered hidden, if it is explicitly hidden
            # or if the field options don't exist
            if field_option_matching is None or field_option_matching.hidden:
                hidden_field_ids.add(field.id)

        return hidden_field_ids

    def enhance_queryset(self, queryset):
        return queryset.prefetch_related("mapviewfieldoptions_set")
