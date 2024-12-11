<template>
  <div class="control__elements">
    <div class="field-multi-polygon">
      <client-only>
        <div id="map" ref="mapContainer" class="map-field-container"></div>
      </client-only>
    </div>
  </div>
</template>

<script>
import maplibregl from "maplibre-gl";
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import {combine as turfCombine} from '@turf/combine'

import rowEditField from '@baserow/modules/database/mixins/rowEditField';

MapboxDraw.constants.classes.CONTROL_BASE = 'maplibregl-ctrl';
MapboxDraw.constants.classes.CONTROL_PREFIX = 'maplibregl-ctrl-';
MapboxDraw.constants.classes.CONTROL_GROUP = 'maplibregl-ctrl-group';

export default {
  mixins: [rowEditField],
  data() {
    return {
      map: null
    };
  },
  async mounted() {
    // Ensure DOM is loaded before initializing the map
    this.$nextTick(() => {
      if (this.$refs.mapContainer) {
        this.initializeMap();
      } else {
        console.error("Map container not found.");
      }
    });
  },
  computed: {},
  methods: {
    initializeMap() {

      // Initialize map
      this.map = new maplibregl.Map({
        container: this.$refs.mapContainer,
        style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        center: [0, 0], // [Longitude, Latitude]
        zoom: 3,
      });

      // Add navigation controls
      this.map.addControl(new maplibregl.NavigationControl({showCompass: false}), "top-right");

      // Initialize draw control
      this.initDrawControl();

      // If the field has a value, draw it on the map
      if (this.value && this.draw) {
        this.draw.add(this.value);
      }
    },
    initDrawControl() {
      this.draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true,
        },
      });

      this.map.addControl(this.draw, 'top-left');

      this.map.on('draw.create', this.updateArea);
      this.map.on('draw.delete', this.updateArea);
      this.map.on('draw.update', this.updateArea);
    },
    updateArea() {
      const featureCollection = this.draw.getAll();
      const combined = turfCombine(featureCollection);

      const multiPolygon = combined.features[0]

      this.$emit('update', multiPolygon);
    },
  },
  beforeDestroy() {
    // Remove the map when the component is destroyed
    if (this.map) this.map.remove();
  },
}
</script>
