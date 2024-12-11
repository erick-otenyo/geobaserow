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
    mapRefreshCount: {
      type: Number,
      required: false,
      default: null
    }
  },
  mounted() {
    this.initializeMap();
  },
  watch: {
    mapRefreshCount: {
      handler() {
        const sourceId = "vector"

        // Remove the tiles for the updated source from the map cache.
        this.map.style.sourceCaches[sourceId].clearTiles();

        // Load the new tiles for the updated source within the current viewport.
        this.map.style.sourceCaches[sourceId].update(this.map.transform);

        // Trigger a repaint of the map to display the updated tiles.
        this.map.triggerRepaint();
      },
    },
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
  