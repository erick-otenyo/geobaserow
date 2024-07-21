# Generated by Django 4.2.13 on 2024-07-20 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0159_linkrowfield_link_row_limit_selection_view"),
        ("geobaserow", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MapView",
            fields=[
                (
                    "view_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.view",
                    ),
                ),
            ],
            options={
                "db_table": "geobaserow_mapview",
            },
            bases=("database.view",),
        ),
        migrations.CreateModel(
            name="MapViewFieldOptions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "hidden",
                    models.BooleanField(
                        default=True,
                        help_text="Whether or not the field should be hidden in the popup.",
                    ),
                ),
                (
                    "order",
                    models.SmallIntegerField(
                        default=32767,
                        help_text="The order that the field has in the view. Lower value is first.",
                    ),
                ),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="database.field"
                    ),
                ),
                (
                    "map_view",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geobaserow.mapview",
                    ),
                ),
            ],
            options={
                "db_table": "geobaserow_mapviewfieldoptions",
                "ordering": ("order", "field_id"),
                "unique_together": {("map_view", "field")},
            },
        ),
        migrations.AddField(
            model_name="mapview",
            name="field_options",
            field=models.ManyToManyField(
                through="geobaserow.MapViewFieldOptions", to="database.field"
            ),
        ),
        migrations.AddField(
            model_name="mapview",
            name="geo_field",
            field=models.ForeignKey(
                blank=True,
                help_text="One of the supported geo fields that the map view will be based on.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="map_view_gep_field",
                to="database.field",
            ),
        ),
    ]
