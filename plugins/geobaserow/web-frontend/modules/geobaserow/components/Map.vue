<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script>
import maplibre from 'maplibre-gl';
import {prepareRequestHeaders} from "@geobaserow/utils";

const defaultStyle = {
  'version': 8,
  "glyphs": "https://tiles.basemaps.cartocdn.com/fonts/{fontstack}/{range}.pbf",
  'sources': {
    'carto-dark': {
      'type': 'raster',
      'tiles': [
        "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
        "https://d.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png"
      ]
    },
    'carto-light': {
      'type': 'raster',
      'tiles': [
        "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png",
        "https://b.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png",
        "https://c.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png",
        "https://d.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png"
      ]
    },
    'voyager': {
      'type': 'raster',
      'tiles': [
        "https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png",
        "https://b.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png",
        "https://c.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png",
        "https://d.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png",

      ]
    },
    'wikimedia': {
      'type': 'raster',
      'tiles': [
        "https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png"
      ]
    },
  },
  'layers': [{
    'id': 'carto-voyager-layer',
    'source': 'voyager',
    'type': 'raster',
    'minzoom': 0,
    'maxzoom': 22
  }]
}


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

      this.map = new maplibre.Map({
        container: this.$refs.mapContainer,
        style: defaultStyle,
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


.map-container {
  width: 100%;
  height: 100%;
}
</style>
  