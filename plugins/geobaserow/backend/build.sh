#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# This file is automatically run by Baserow when the plugin is installed. This can
# happen both inside a Dockerfile as part of the build process or when a Baserow
# container is already running.

# Baserow will automatically install this python module for you so you should not
# repeat any python dependency installation steps here.

# Instead this file is ideal for any other installation custom steps here required by
# your plugin. For example installing a postgres extension used by your plugin.

apt update
if [[ "${BASEROW_EMBEDDED_PSQL:-}" != "false" && "${BASEROW_IMAGE_TYPE:-}"  == "all-in-one" ]]; then
  # Only install the extension when we haven't explicitly said we aren't using the
  # embedded psql and we are in the all-in-one image where we know there is an embedded
  # psql

  echo "Installing postgis extension into the image/container..."
  apt-get -y --no-install-recommends install \
    postgresql-15-postgis-3 \
    postgresql-15-postgis-3-scripts \
    binutils \
    libproj-dev \
    gdal-bin
else
  # Otherwise just install the runtime dependencies
  echo "WARNING: to use the baserow_geo_plugin with an external postgresql server you must ensure you have installed and enabled the postgis postgres extension manually."
  apt-get -y --no-install-recommends install binutils libproj-dev gdal-bin
fi

apt-get autoclean
apt-get clean
apt-get autoremove
rm -rf /var/lib/apt/lists/*
