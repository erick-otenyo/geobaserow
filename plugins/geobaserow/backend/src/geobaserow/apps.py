from baserow.core.registries import plugin_registry
from django.apps import AppConfig

from loguru import logger


class PluginNameConfig(AppConfig):
    name = "geobaserow"
    
    def ready(self):
        from baserow.contrib.database.fields.registries import field_type_registry
        from baserow.contrib.database.views.registries import view_type_registry
        from baserow.core.jobs.registries import job_type_registry
        from baserow.core.action.registries import action_type_registry
        
        from .plugins import PluginNamePlugin
        from .views.view_types import MapViewType
        from .fields.field_types import PointFieldType, MultiPolygonFieldType
        from .file_import.job_types import GeoFileImportJobType
        from .table.actions import CreateGeoTableActionType
        
        plugin_registry.register(PluginNamePlugin())
        
        field_type_registry.register(PointFieldType())
        field_type_registry.register(MultiPolygonFieldType())
        
        view_type_registry.register(MapViewType())
        
        action_type_registry.register(CreateGeoTableActionType())
        
        if job_type_registry.get("file_import") is not None:
            # monkey patch "file_import" job type to support GeoJSON files
            instance = GeoFileImportJobType()
            job_type_registry.registry["file_import"] = instance
            instance.after_register()
