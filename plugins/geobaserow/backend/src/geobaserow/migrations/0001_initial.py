from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("database", "0073_increase_available_number_dp"),
    ]

    operations = [
        migrations.CreateModel(
            name="PointField",
            fields=[
                (
                    "field_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=models.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="database.Field",
                    ),
                ),
            ],
            bases=("database.field",),
        ),
    ]
