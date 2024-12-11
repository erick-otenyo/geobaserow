<template>
  <div id="map" ref="mapContainer" class="map-field-container point-input"></div>
</template>
<script>

import maplibregl from "maplibre-gl";

export default {
  name: "MapPointInput",
  props: {
    latLng: {
      type: Object,
    },
    basemap: {
      type: String,
      default: "voyager",
    },
  },
  mounted() {
    this.initializeMap();
  },
  watch: {
    basemap(newValue, oldValue) {
      this.map.setStyle(`https://basemaps.cartocdn.com/gl/${this.basemap}-gl-style/style.json`);
    },
    latLng(newValue, oldValue) {
      this.createOrUpdateMarker()
    },
  },
  methods: {
    initializeMap() {
      const basemapStyle = `https://basemaps.cartocdn.com/gl/${this.basemap}-gl-style/style.json`;

      // Initialize map
      this.map = new maplibregl.Map({
        container: this.$refs.mapContainer,
        style: basemapStyle,
        center: [0, 0], // [Longitude, Latitude]
        zoom: 3,
        minZoom: 1,
        maxZoom: 20,
      });

      // Add navigation controls
      this.map.addControl(new maplibregl.NavigationControl({showCompass: false}), "top-right");

      // Add a marker to the map
      this.createOrUpdateMarker()

      // on map click, update marker
      this.map.on('click', this.onMapClick);

    },

    createOrUpdateMarker() {
      if (!this.marker) {
        this.marker = new maplibregl.Marker({draggable: true})
            .setLngLat([this.latLng.lng, this.latLng.lat])
            .addTo(this.map);

        this.marker.on('dragend', this.onDragEnd);
      } else {
        this.marker.setLngLat([this.latLng.lng, this.latLng.lat])
      }

      this.centerMap(this.latLng)
    },

    onMapClick(e) {
      const lngLat = e.lngLat;
      this.onChange(lngLat)
    },

    onDragEnd() {
      const lngLat = this.marker.getLngLat();
      this.onChange(lngLat)
    },

    onChange(lngLat) {
      this.$emit('change', lngLat)
    },

    centerMap(latLng) {
      if (latLng) {
        this.map.panTo([latLng.lng, latLng.lat])
      }
    },
  },
}
</script>

<style>

.point-input {
  height: 200px;
}

</style>