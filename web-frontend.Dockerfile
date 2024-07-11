FROM baserow/web-frontend:1.26.0

USER root

COPY ./plugins/geobaserow/ /baserow/plugins/geobaserow/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/geobaserow

USER $UID:$GID
