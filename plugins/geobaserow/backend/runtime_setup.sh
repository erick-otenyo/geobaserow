#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# This file is automatically run by Baserow when the plugin is built into a Dockerfile.
# It will also be called when building the plugin in an existing container. You should
# only perform build steps in this script which make sense run in a Dockerfile.

# Any install steps that will modify things in Baserow's data volume should instead
# be done in the runtime_setup.sh script next to this one. For example running some
# SQL against the embedded postgres database should not be done in this script as it
# makes no sense to do that in a Dockerfile build.

# Baserow will automatically install this python module for you so you should not
# repeat any python dependency installation steps here.

# Instead this file is ideal for any other installation custom steps here required by
# your plugin. For example installing a postgres extension used by your plugin.

if [[ "${BASEROW_EMBEDDED_PSQL:-}" != "false" && "${BASEROW_IMAGE_TYPE:-}"  == "all-in-one" ]]; then
  # We use this helper script present in the baserow/baserow image to run SQL against
  # the database as a superuser which is required and why we can't do this in a
  # migration.
  /baserow/supervisor/docker-postgres-setup.sh run <<-'EOSQL'
			CREATE EXTENSION IF NOT EXISTS postgis;
		EOSQL
else
  echo "WARNING: to use the baserow_geo_plugin with an external postgresql server you must ensure you have installed and enabled the postgis postgres extension manually."
fi
