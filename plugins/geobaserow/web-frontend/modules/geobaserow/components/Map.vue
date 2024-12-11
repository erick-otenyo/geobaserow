<template>
  <div ref="mapContainer" class="map-view-container"></div>
</template>

<script>
import maplibregl from 'maplibre-gl';

import {prepareRequestHeaders} from "@geobaserow/utils";

export default {
  name: 'Map',
  props: {
    tileUrl: {
      type: String,
      required: false,
      default: null,
    },
  },
  mounted() {
    this.initializeMap();
  },
  methods: {
    initializeMap() {

      const baseURL = this.$client.defaults.baseURL
      const headers = prepareRequestHeaders(this.$store)

      this.map = new maplibregl.Map({
        container: this.$refs.mapContainer,
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: [0, 0],
        zoom: 2,
        // adding authorization to tile urls
        transformRequest: (url, resourceType) => {
          if (url.startsWith(baseURL)) {
            return {
              url: url,
              headers: {
                ...headers
              },
              credentials: 'include'
            };
          }
        }
      });

      // Add navigation controls
      this.map.addControl(new maplibregl.NavigationControl({showCompass: false}), "top-right");


      this.map.on("load", () => {
        if (this.tileUrl) {
          // add source
          this.map.addSource("vector", {
                type: "vector",
                tiles: [this.tileUrl],
              }
          )
          // add layer
          this.map.addLayer({
            'id': 'vector',
            'type': 'circle',
            'source': 'vector',
            "source-layer": "default",
            'paint': {
              'circle-color': "#000",
              'circle-radius': 10,
            }
          });
        }
      })
    },
  },
};
</script>

<style>
.map-view-container {
  width: 100%;
  height: 100%;
}
</style>
  