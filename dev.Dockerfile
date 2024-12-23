# This a dev image for testing your plugin when installed into the Baserow all-in-one image
FROM baserow/baserow:1.29.3 AS base

FROM baserow/baserow:1.29.3

ARG PLUGIN_BUILD_UID
ENV PLUGIN_BUILD_UID=${PLUGIN_BUILD_UID:-9999}
ARG PLUGIN_BUILD_GID
ENV PLUGIN_BUILD_GID=${PLUGIN_BUILD_GID:-9999}

# Use a multi-stage copy to quickly chown the contents of Baserow to match the user
# that will be running this image.
COPY --from=base --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID /baserow /baserow

RUN groupmod -o -g $PLUGIN_BUILD_GID baserow_docker_group && usermod -u $PLUGIN_BUILD_UID $DOCKER_USER

# Install your dev dependencies manually.
COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/geobaserow/backend/requirements/dev.txt /tmp/plugin-dev-requirements.txt
ENV PIP_CACHE_DIR=/tmp/baserow_pip_cache
RUN --mount=type=cache,mode=777,target=$PIP_CACHE_DIR,uid=$UID,gid=$GID . /baserow/venv/bin/activate && \
    pip3 install -r /tmp/plugin-dev-requirements.txt && chown -R $PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID /baserow/venv

COPY --chown=$PLUGIN_BUILD_UID:$PLUGIN_BUILD_GID ./plugins/geobaserow/ $BASEROW_PLUGIN_DIR/geobaserow/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/geobaserow --dev

ENV PATH="/baserow/venv/bin:$PATH"

ENV BASEROW_ALL_IN_ONE_DEV_MODE='true'
