import json

from baserow.contrib.database.file_import.job_types import FileImportJobType
from baserow.contrib.database.rows.actions import ImportRowsActionType
from baserow.contrib.database.rows.exceptions import ReportMaxErrorCountExceeded
from baserow.core.action.registries import action_type_registry
from django.db import transaction
from geobaserow.table.actions import CreateGeoTableActionType
from geobaserow.table.exceptions import UnsupportedGeoType, InvalidGeoJSONFeature


class GeoFileImportJobType(FileImportJobType):
    type = "file_import"
    
    job_exceptions_map = {
        **FileImportJobType.job_exceptions_map,
        UnsupportedGeoType: "The provided file contains an unsupported geometry type.",
        InvalidGeoJSONFeature: "The provided file contains an invalid GeoJSON feature.",
    }
    
    def run(self, job, progress):
        """
        Fills the provided table with the normalized data that needs to be created upon
        creation of the table.
        """
        
        with job.data_file.open("r") as fin:
            data = json.load(fin)
        
        try:
            if job.table is None:
                new_table, error_report = action_type_registry.get_by_type(
                    CreateGeoTableActionType
                ).do(
                    job.user,
                    job.database,
                    name=job.name,
                    data=data,
                    first_row_header=job.first_row_header,
                    progress=progress,
                )
                
                job.table = new_table
                job.save(update_fields=("table",))
            else:
                _, error_report = action_type_registry.get_by_type(
                    ImportRowsActionType
                ).do(
                    job.user,
                    table=job.table,
                    data=data,
                    progress=progress,
                )
        # when a job handler fails, celery worker will not commit and `after_commit`
        # won't be called. That's why we need to catch this specific error and
        # perform a bit of cleanup on the job.
        except ReportMaxErrorCountExceeded as err:
            self.cleanup_job(job, err.report)
            raise
        except Exception:
            raise
        
        def after_commit():
            """
            Removes the data file to save space and save the error report.

            This will be executed when a job finished successfully.
            """
            
            self.cleanup_job(job, error_report)
        
        transaction.on_commit(after_commit)
