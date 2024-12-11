import json
from typing import Any, List, Tuple

from baserow.contrib.database.fields.constants import RESERVED_BASEROW_FIELD_NAMES
from baserow.contrib.database.fields.exceptions import (
    InvalidBaserowFieldName,
    MaxFieldLimitExceeded,
    MaxFieldNameLengthExceeded,
    ReservedBaserowFieldNameException,
)
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.table.exceptions import (
    InitialTableDataDuplicateName,
    InitialTableDataLimitExceeded,
    InvalidInitialTableData,
)
from baserow.contrib.database.table.handler import TableHandler
from django.conf import settings
from django.utils.translation import gettext as _

from .exceptions import UnsupportedGeoType, InvalidGeoJSONFeature


class GeoTableHandler(TableHandler):
    def normalize_initial_table_data(
            self, data: List[List[Any]], first_row_header: bool
    ) -> Tuple[List, List]:
        """
        Normalizes the provided initial table data. The amount of columns will be made
        equal for each row. The header and the rows will also be separated.

        :param data: A list containing all the provided rows.
        :param first_row_header: Indicates if the first row is the header. For each
            of these header columns a field is going to be created.
        :raises InvalidInitialTableData: When the data doesn't contain a column or row.
        :raises MaxFieldNameLengthExceeded: When the provided name is too long.
        :raises InitialTableDataDuplicateName: When duplicates exit in field names.
        :raises ReservedBaserowFieldNameException: When the field name is reserved by
            Baserow.
        :raises InvalidBaserowFieldName: When the field name is invalid (empty).
        :return: A list containing the field names with a type and a list containing all
            the rows.
        """
        
        if len(data) == 0:
            raise InvalidInitialTableData("At least one row should be provided.")
        
        limit = settings.INITIAL_TABLE_DATA_LIMIT
        if limit and len(data) > limit:
            raise InitialTableDataLimitExceeded(
                f"It is not possible to import more than "
                f"{settings.INITIAL_TABLE_DATA_LIMIT} rows when creating a table."
            )
        
        largest_column_count = len(max(data, key=len))
        
        if largest_column_count == 0:
            raise InvalidInitialTableData("At least one column should be provided.")
        
        fields = data.pop(0) if first_row_header else []
        
        for i in range(len(fields), largest_column_count):
            fields.append(_("Field %d") % (i + 1,))
        
        if len(fields) > settings.MAX_FIELD_LIMIT:
            raise MaxFieldLimitExceeded(
                f"Fields count exceeds the limit of {settings.MAX_FIELD_LIMIT}"
            )
        
        # Stripping whitespace from field names is already done by
        # TableCreateSerializer however we repeat to ensure that non API usages of
        # this method is consistent with api usage.
        field_name_set = {str(name).strip() for name in fields}
        
        if len(field_name_set) != len(fields):
            raise InitialTableDataDuplicateName()
        
        max_field_name_length = Field.get_max_name_length()
        long_field_names = [x for x in field_name_set if len(x) > max_field_name_length]
        
        if len(long_field_names) > 0:
            raise MaxFieldNameLengthExceeded(max_field_name_length)
        
        if len(field_name_set.intersection(RESERVED_BASEROW_FIELD_NAMES)) > 0:
            raise ReservedBaserowFieldNameException()
        
        if "" in field_name_set:
            raise InvalidBaserowFieldName()
        
        geo_col_idx = None
        
        fields_with_type = []
        for f_idx, field_name in enumerate(fields):
            field_type = "text"
            if field_name.lower() in ["geometry"]:
                geo_col_idx = f_idx
                sample_val = data[0][f_idx]
                
                try:
                    geo_type = sample_val.get("type")
                except json.JSONDecodeError:
                    raise InvalidGeoJSONFeature("Invalid GeoJSON feature")
                
                if geo_type == "Point":
                    field_type = "point"
                else:
                    raise UnsupportedGeoType(f"Unsupported GeoJSON type: {geo_type}")
            
            fields_with_type.append((field_name, field_type, {}))
        
        result = []
        
        for row in data:
            result_row = []
            for idx, value in enumerate(row):
                if geo_col_idx == geo_col_idx:
                    result_row.append(value)
                else:
                    result_row.append(str(value))
            
            result.append(result_row)
        
        return fields_with_type, result
