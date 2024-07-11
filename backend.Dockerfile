FROM baserow/backend:1.26.0

USER root

COPY ./plugins/geobaserow/ $BASEROW_PLUGIN_DIR/geobaserow/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/geobaserow

USER $UID:$GID
