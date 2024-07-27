from django.urls import re_path

from .views import MapViewView

app_name = "geobaserow.api.views.map"

urlpatterns = [
    re_path(r"(?P<view_id>[0-9]+)/tiles/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)/$", MapViewView.as_view(),
            name="mvt_tiles"),
]
