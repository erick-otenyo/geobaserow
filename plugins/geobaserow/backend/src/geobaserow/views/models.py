from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.views.models import View
from baserow.core.mixins import HierarchicalModelMixin
from django.db import models
from django.db.models import Q


class MapView(View):
    field_options = models.ManyToManyField(Field, through="MapViewFieldOptions")
    geo_field = models.ForeignKey(
        Field,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="map_view_gep_field",
        help_text="One of the supported geo fields that "
                  "the map view will be based on.",
    )
    
    class Meta:
        db_table = "geobaserow_mapview"


class MapViewFieldOptionsManager(models.Manager):
    """
    The View can be trashed and the field options are not deleted, therefore
    we need to filter out the trashed views.
    """
    
    def get_queryset(self):
        trashed_Q = Q(map_view__trashed=True) | Q(field__trashed=True)
        return super().get_queryset().filter(~trashed_Q)


class MapViewFieldOptions(HierarchicalModelMixin, models.Model):
    objects = MapViewFieldOptionsManager()
    objects_and_trash = models.Manager()
    
    map_view = models.ForeignKey(MapView, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    hidden = models.BooleanField(
        default=True,
        help_text="Whether or not the field should be hidden in the popup.",
    )
    # The default value is the maximum value of the small integer field because a newly
    # created field must always be last.
    order = models.SmallIntegerField(
        default=32767,
        help_text="The order that the field has in the view. Lower value is first.",
    )
    
    def get_parent(self):
        return self.map_view
    
    class Meta:
        db_table = "geobaserow_mapviewfieldoptions"
        ordering = ("order", "field_id")
        unique_together = ("map_view", "field")
