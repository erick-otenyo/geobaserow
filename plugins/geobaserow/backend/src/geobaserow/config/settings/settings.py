# Imported automatically by the Baserow backend before after other django settings files
# are imported.


def setup(settings):
    settings.INSTALLED_APPS += ["django.contrib.gis", "rest_framework_gis"]
    
    for db, value in settings.DATABASES.items():
        settings.DATABASES[db]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
    
    settings.CORS_ORIGIN_ALLOW_ALL = False
    settings.CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]
    
    settings.CORS_ALLOW_CREDENTIALS = True
