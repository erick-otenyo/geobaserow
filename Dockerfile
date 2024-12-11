FROM baserow/baserow:1.29.3

COPY ./plugins/geobaserow/ /baserow/plugins/geobaserow/
RUN /baserow/plugins/install_plugin.sh --folder /baserow/plugins/geobaserow
