from collections import OrderedDict
from http.client import responses

from baserow.api.decorators import (
    allowed_includes,
    map_exceptions,
    validate_query_parameters,
)
from baserow.api.errors import ERROR_USER_NOT_IN_GROUP
from baserow.api.schemas import get_error_schema
from baserow.api.search.serializers import SearchQueryParamSerializer
from baserow.api.serializers import get_example_pagination_serializer_class
from baserow.contrib.database.api.constants import SEARCH_MODE_API_PARAM
from baserow.contrib.database.api.fields.errors import (
    ERROR_FILTER_FIELD_NOT_FOUND,
    ERROR_ORDER_BY_FIELD_NOT_FOUND,
    ERROR_ORDER_BY_FIELD_NOT_POSSIBLE,
)
from baserow.contrib.database.api.rows.serializers import (
    RowSerializer,
    get_example_row_metadata_field_serializer,
    get_example_row_serializer_class,
    get_row_serializer_class,
)
from baserow.contrib.database.api.views.errors import (
    ERROR_VIEW_FILTER_TYPE_DOES_NOT_EXIST,
    ERROR_VIEW_FILTER_TYPE_UNSUPPORTED_FIELD,
)
from baserow.contrib.database.api.views.gallery.serializers import (
    GalleryViewFieldOptionsSerializer,
)
from baserow.contrib.database.api.views.serializers import FieldOptionsField
from baserow.contrib.database.fields.exceptions import (
    FilterFieldNotFound,
    OrderByFieldNotFound,
    OrderByFieldNotPossible,
)
from baserow.contrib.database.rows.registries import row_metadata_registry
from baserow.contrib.database.table.operations import ListRowsDatabaseTableOperationType
from baserow.contrib.database.views.exceptions import (
    ViewDoesNotExist,
    ViewFilterTypeDoesNotExist,
    ViewFilterTypeNotAllowedForField,
)
from baserow.contrib.database.views.handler import ViewHandler
from baserow.contrib.database.views.registries import (
    view_type_registry,
)
from baserow.contrib.database.views.signals import view_loaded
from baserow.core.exceptions import UserNotInWorkspace
from baserow.core.handler import CoreHandler
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema
from geobaserow.views.models import MapView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from geobaserow.views.exceptions import MapViewHasNoGeoField

from .errors import ERROR_MAP_DOES_NOT_EXIST


class MapViewView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="view_id",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.INT,
                description="Returns only rows that belong to the related view's "
                            "table.",
            ),
            OpenApiParameter(
                name="include",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description=(
                        "A comma separated list allowing the values of `field_options` and "
                        "`row_metadata` which will add the object/objects with the same "
                        "name to the response if included. The `field_options` object "
                        "contains user defined view settings for each field. For example "
                        "the field's width is included in here. The `row_metadata` object"
                        " includes extra row specific data on a per row basis."
                ),
            ),
            OpenApiParameter(
                name="limit",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                description="Defines how many rows should be returned.",
            ),
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="If provided only rows with data that matches the search "
                            "query are going to be returned.",
            ),
            SEARCH_MODE_API_PARAM,
        ],
        tags=["Database table map view"],
        operation_id="list_database_table_map_view_rows",
        description=(
                "Lists the requested rows of the view's table related to the provided "
                "`view_id` if the authorized user has access to the database's workspace. "
                "The response is paginated by a limit/offset style."
        ),
        responses={
            200: get_example_pagination_serializer_class(
                get_example_row_serializer_class(
                    example_type="get", user_field_names=False
                ),
                additional_fields={
                    "field_options": FieldOptionsField(
                        serializer_class=GalleryViewFieldOptionsSerializer,
                        required=False,
                    ),
                    "row_metadata": get_example_row_metadata_field_serializer(),
                },
                serializer_name="PaginationSerializerWithGalleryViewFieldOptions",
            ),
            400: get_error_schema(
                [
                    "ERROR_USER_NOT_IN_GROUP",
                    "ERROR_FILTER_FIELD_NOT_FOUND",
                    "ERROR_VIEW_FILTER_TYPE_DOES_NOT_EXIST",
                    "ERROR_VIEW_FILTER_TYPE_UNSUPPORTED_FIELD",
                    "ERROR_FILTERS_PARAM_VALIDATION_ERROR",
                    "ERROR_ORDER_BY_FIELD_NOT_FOUND",
                    "ERROR_ORDER_BY_FIELD_NOT_POSSIBLE",
                ]
            ),
            404: get_error_schema(["ERROR_MAP_DOES_NOT_EXIST"]),
        },
    )
    @map_exceptions(
        {
            UserNotInWorkspace: ERROR_USER_NOT_IN_GROUP,
            ViewDoesNotExist: ERROR_MAP_DOES_NOT_EXIST,
            FilterFieldNotFound: ERROR_FILTER_FIELD_NOT_FOUND,
            ViewFilterTypeDoesNotExist: ERROR_VIEW_FILTER_TYPE_DOES_NOT_EXIST,
            ViewFilterTypeNotAllowedForField: ERROR_VIEW_FILTER_TYPE_UNSUPPORTED_FIELD,
            OrderByFieldNotFound: ERROR_ORDER_BY_FIELD_NOT_FOUND,
            OrderByFieldNotPossible: ERROR_ORDER_BY_FIELD_NOT_POSSIBLE,
        }
    )
    @allowed_includes("field_options", "row_metadata")
    @validate_query_parameters(SearchQueryParamSerializer, return_validated=True)
    def get(
            self,
            request: Request,
            view_id: int,
            field_options: bool,
            row_metadata: bool,
            query_params,
    ):
        """Responds with the rows for the map view."""

        view_handler = ViewHandler()
        view = view_handler.get_view_as_user(request.user, view_id, MapView, )
        view_type = view_type_registry.get_by_model(view)
        workspace = view.table.database.workspace

        CoreHandler().check_permissions(
            request.user,
            ListRowsDatabaseTableOperationType.type,
            workspace=workspace,
            context=view.table,
        )

        geo_field = view.geo_field
        if not geo_field:
            raise MapViewHasNoGeoField(
                "The requested map view does not have a required geo field."
            )

        search = query_params.get("search")
        search_mode = query_params.get("search_mode")

        model = view.table.get_model()
        queryset = view_handler.get_queryset(
            view,
            search,
            model,
            search_mode=search_mode,
        )

        serializer_class = get_row_serializer_class(
            model, RowSerializer, is_response=True
        )
        serializer = serializer_class(queryset, many=True)

        response = Response(OrderedDict([
            ('count', queryset.count()),
            ('results', serializer.data)
        ]))

        if field_options:
            context = {"fields": [o["field"] for o in model._field_objects.values()]}
            serializer_class = view_type.get_field_options_serializer_class(
                create_if_missing=True
            )
            response.data.update(**serializer_class(view, context=context).data)

        if row_metadata:
            row_metadata = row_metadata_registry.generate_and_merge_metadata_for_rows(
                request.user, view.table, (row.id for row in queryset)
            )
            response.data.update(row_metadata=row_metadata)

        view_loaded.send(
            sender=self,
            table=view.table,
            view=view,
            table_model=model,
            user=request.user,
        )

        return response
