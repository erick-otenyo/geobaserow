#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# This file is automatically run by Baserow when the plugin is uninstalled.

# Baserow will automatically `pip uninstall` the plugin for you so no need to do that
# in here.

# If you plugin has applied any migrations you should run
# `./baserow migrate baserow_geo_plugin zero` here to undo any changes
# made to the database.

if [[ "${BASEROW_EMBEDDED_PSQL:-}" != "false" && "${BASEROW_IMAGE_TYPE:-}"  == "all-in-one" ]]; then
  apt-get uninstall -y \
    postgresql-11-postgis-2.5 \
    postgresql-11-postgis-2.5-scripts \
    binutils \
    libproj-dev \
    gdal-bin
  /baserow/supervisor/docker-postgres-setup.sh run <<-'EOSQL'
			DROP EXTENSION IF EXISTS postgis;
		EOSQL
else
  apt-get uninstall -y \
    binutils \
    libproj-dev \
    gdal-bin
fi
