from baserow.contrib.database.fields.models import Field
from django.db import models


class BaseGeoFieldMixin(models.Model):
    BASEMAP_CHOICES = [
        ("voyager", "Voyager - Colored map"),
        ("positron", "Positron - Light gray map"),
        ("dark-matter", "Dark Matter - Dark gray map"),
    ]
    
    default_center_lat = models.FloatField(default=0, help_text="The default center latitude of the map.")
    default_center_lon = models.FloatField(default=0, help_text="The default center longitude of the map.")
    default_zoom = models.IntegerField(default=4, help_text="The default zoom level of the map.")
    basemap = models.CharField(max_length=255, choices=BASEMAP_CHOICES, default="voyager",
                               help_text="The basemap of the map.")
    
    class Meta:
        abstract = True


class PointField(Field, BaseGeoFieldMixin):
    pass


class MultiPolygonField(Field, BaseGeoFieldMixin):
    pass
