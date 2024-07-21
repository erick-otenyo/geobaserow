from baserow.core.registries import plugin_registry
from django.apps import AppConfig


class PluginNameConfig(AppConfig):
    name = "geobaserow"

    def ready(self):
        from baserow.contrib.database.fields.registries import field_type_registry
        from baserow.contrib.database.views.registries import view_type_registry

        from .plugins import PluginNamePlugin
        from .views.view_types import MapViewType
        from .fields.field_types import PointFieldType

        plugin_registry.register(PluginNamePlugin())

        field_type_registry.register(PointFieldType())
        view_type_registry.register(MapViewType())
