<template>
  <div class="control__elements">
    <div class="field-point">
      <client-only>
        <div id="map" ref="mapContainer" class="map-field-container"></div>
      </client-only>
    </div>
  </div>
</template>

<script>
import maplibregl from "maplibre-gl";
import rowEditField from '@baserow/modules/database/mixins/rowEditField'

export default {
  mixins: [rowEditField],
  data() {
    return {
      map: null
    };
  },
  mounted() {
    // Ensure DOM is loaded before initializing the map
    this.$nextTick(() => {
      if (this.$refs.mapContainer) {
        this.initializeMap();
      }
    });
  },
  computed: {
    latLng() {
      if (this.value && this.value.coordinates) {
        return {lng: this.value.coordinates[0], lat: this.value.coordinates[1]}
      }
      return null
    }
  },
  methods: {
    initializeMap() {
      const {basemap, default_center_lat, default_center_lon, default_zoom} = this.field
      const style = basemap ? `https://basemaps.cartocdn.com/gl/${basemap}-gl-style/style.json` : "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"

      // Initialize map
      this.map = new maplibregl.Map({
        container: this.$refs.mapContainer,
        style: style,
        center: [default_center_lon, default_center_lat], // [Longitude, Latitude]
        zoom: default_zoom,
      });

      // Add navigation controls
      this.map.addControl(new maplibregl.NavigationControl({showCompass: false}), "top-right");

      if (this.latLng && this.latLng.lat && this.latLng.lng) {
        this.createOrUpdateMarker(this.latLng)
      }

      // on map click, update marker
      this.map.on('click', this.onMapClick);
    },
    createOrUpdateMarker(latLng) {
      if (!this.marker) {
        this.marker = new maplibregl.Marker({draggable: true})
            .setLngLat([latLng.lng, latLng.lat])
            .addTo(this.map);

        this.marker.on('dragend', this.onDragEnd);
      } else {
        this.marker.setLngLat([latLng.lng, latLng.lat])
      }
      this.centerMap(latLng)
    },
    onMapClick(e) {
      if (this.readOnly) {
        return
      }
      this.addOrUpdatePoint(e.lngLat)
    },
    onDragEnd() {
      const lngLat = this.marker.getLngLat();

      this.addOrUpdatePoint(lngLat)
    },
    centerMap(latLng) {
      if (latLng) {
        this.map.panTo([latLng.lng, latLng.lat])
      }
    },

    addOrUpdatePoint(lngLat) {
      if (this.readOnly) {
        return
      }

      this.createOrUpdateMarker(lngLat)

      const point = {
        "type": "Point",
        "coordinates": [lngLat.lng, lngLat.lat],
      }

      this.$emit('update', point, {lat: lngLat.lat, lng: lngLat.lng})

      this.centerMap({lng: lngLat.lng, lat: lngLat.lat})
    },
  },
  beforeDestroy() {
    // Remove the map when the component is destroyed
    if (this.map) this.map.remove();
  },

}
</script>
