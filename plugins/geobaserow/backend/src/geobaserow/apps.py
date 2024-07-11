from baserow.core.registries import plugin_registry
from django.apps import AppConfig


class PluginNameConfig(AppConfig):
    name = "geobaserow"

    def ready(self):
        from .plugins import PluginNamePlugin

        plugin_registry.register(PluginNamePlugin())

        from baserow.contrib.database.fields.registries import field_type_registry

        from .field_types import PointFieldType

        field_type_registry.register(PointFieldType())
