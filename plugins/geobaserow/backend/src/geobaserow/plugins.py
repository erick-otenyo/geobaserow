from baserow.core.registries import Plugin
from django.urls import path, include

from .api import urls as api_urls


class PluginNamePlugin(Plugin):
    type = "geobaserow"

    def get_api_urls(self):
        return [
            path(
                "geobaserow/",
                include(api_urls, namespace=self.type),
            ),
        ]
