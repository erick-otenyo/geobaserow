from rest_framework import serializers
from baserow.contrib.database.table.models import Table


class GeoTableCreateSerializer(serializers.ModelSerializer):
    data = serializers.ListField(
        min_length=1,
        default=None,
        help_text=(
            "A list of rows that needs to be created as initial table data. "
            "Each row is a list of values that are going to be added in the new "
            "table in the same order as provided.\n\n"
            'Ex: \n```json\n[\n  ["row1_field1_value", "row1_field2_value"],\n'
            '  ["row2_field1_value", "row2_field2_value"],\n]\n```\n'
            "for creating a two rows table with two fields.\n\n"
            "If not provided, some example data is going to be created."
        ),
    )
    job_type_name = serializers.CharField(
        default=None,
        help_text="Indicates the type of jon to use for the table creation.",
    )
    
    class Meta:
        model = Table
        fields = ("name", "data", "job_type_name")
        extra_kwargs = {
            "data": {"required": False},
            "job_type_name": {"required": False},
        }
