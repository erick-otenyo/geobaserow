FROM baserow/backend:1.29.3

USER root

COPY ./plugins/geobaserow/ $BASEROW_PLUGIN_DIR/geobaserow/
RUN /baserow/plugins/install_plugin.sh --folder $BASEROW_PLUGIN_DIR/geobaserow

USER $UID:$GID
