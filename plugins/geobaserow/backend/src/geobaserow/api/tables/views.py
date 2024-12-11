from baserow.api.decorators import validate_body
from baserow.api.jobs.serializers import JobSerializer
from baserow.contrib.database.api.tables.views import AsyncCreateTableView
from baserow.contrib.database.handler import DatabaseHandler
from baserow.contrib.database.operations import (
    CreateTableDatabaseTableOperationType,
)
from baserow.core.handler import CoreHandler
from baserow.core.jobs.handler import JobHandler
from baserow.core.jobs.registries import job_type_registry
from rest_framework.response import Response

from .serializers import GeoTableCreateSerializer


class AsyncCreateGeoTableView(AsyncCreateTableView):
    @validate_body(GeoTableCreateSerializer)
    def post(self, request, data, database_id):
        """Creates a job to create a new table in a database."""
        
        database = DatabaseHandler().get_database(database_id)
        
        CoreHandler().check_permissions(
            request.user,
            CreateTableDatabaseTableOperationType.type,
            workspace=database.workspace,
            context=database,
        )
        
        file_import_job = JobHandler().create_and_start_job(
            request.user,
            data["job_type_name"],
            database=database,
            name=data["name"],
            data=data["data"],
            sync=True if data["data"] is None else False,
        )
        
        serializer = job_type_registry.get_serializer(file_import_job, JobSerializer)
        return Response(serializer.data)
