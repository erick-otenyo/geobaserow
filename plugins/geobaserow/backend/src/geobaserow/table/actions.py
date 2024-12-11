from typing import Any, List, Optional

from baserow.contrib.database.models import Database
from baserow.contrib.database.table.actions import CreateTableActionType
from .handler import GeoTableHandler
from baserow.contrib.database.table.models import Table
from baserow.core.utils import Progress
from django.contrib.auth.models import AbstractUser


class CreateGeoTableActionType(CreateTableActionType):
    type = "create_geo_table"
    
    @classmethod
    def do(
            cls,
            user: AbstractUser,
            database: Database,
            name: str,
            data: Optional[List[List[Any]]] = None,
            first_row_header: bool = True,
            progress: Optional[Progress] = None,
    ) -> Table:
        """
        Create a table in the specified database.
        Undoing this action trashes the table and redoing restores it.

        :param user: The user on whose behalf the table is created.
        :param database: The database that the table instance belongs to.
        :param name: The name of the table is created.
        :param data: A list containing all the rows that need to be inserted is
            expected. All the values will be inserted in the database.
        :param first_row_header: Indicates if the first row are the fields. The names
            of these rows are going to be used as fields. If `fields` is provided,
            this options is ignored.
        :param progress: An optional progress instance if you want to track the progress
            of the task.
        :return: The created table and the error report.
        """
        
        table, error_report = GeoTableHandler().create_table(
            user,
            database,
            name,
            data=data,
            first_row_header=first_row_header,
            fill_example=True,
            progress=progress,
        )
        
        workspace = database.workspace
        params = cls.Params(database.id, database.name, table.id, table.name)
        cls.register_action(user, params, cls.scope(database.id), workspace=workspace)
        
        return table, error_report
